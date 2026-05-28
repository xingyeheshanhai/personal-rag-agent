from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, UploadFile, status

from app.core.config import settings
from app.schemas.document import DocumentSearchResponse, DocumentUploadResponse
from app.services.document_loader import UnsupportedDocumentTypeError
from app.services.document_processor import parse_document_to_chunks
from app.services.vector_store import add_document_chunks, search_documents


router = APIRouter()

ALLOWED_FILE_TYPES = {
    ".pdf": "pdf",
    ".md": "markdown",
    ".markdown": "markdown",
    ".txt": "txt",
    ".docx": "word",
}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile) -> DocumentUploadResponse:
    original_name = Path(file.filename or "").name
    suffix = Path(original_name).suffix.lower()
    file_type = ALLOWED_FILE_TYPES.get(suffix)

    if not original_name or file_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Allowed types: PDF, Markdown, TXT, DOCX.",
        )

    upload_dir = Path(settings.upload_directory)
    upload_dir.mkdir(parents=True, exist_ok=True)

    doc_id = uuid4().hex
    saved_name = f"{doc_id}_{original_name}"
    saved_path = upload_dir / saved_name
    file_size = 0

    try:
        with saved_path.open("wb") as output_file:
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)
                if file_size > settings.max_upload_size_bytes:
                    output_file.close()
                    saved_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File too large. Maximum upload size is 20MB.",
                    )
                output_file.write(chunk)
    finally:
        await file.close()

    try:
        chunks = parse_document_to_chunks(
            saved_path,
            doc_id=doc_id,
            source_file=original_name,
        )
    except UnsupportedDocumentTypeError as exc:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse document: {exc}",
        ) from exc

    try:
        add_document_chunks(chunks)
    except Exception as exc:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store document chunks: {exc}",
        ) from exc

    return DocumentUploadResponse(
        doc_id=doc_id,
        file_name=original_name,
        file_type=file_type,
        file_size=file_size,
        saved_path=str(saved_path),
        chunk_count=len(chunks),
        chunks=chunks,
        status="uploaded",
    )


@router.get("/search", response_model=DocumentSearchResponse)
async def search_uploaded_documents(
    query: str = Query(..., min_length=1),
    top_k: int = Query(default=5, ge=1, le=20),
) -> DocumentSearchResponse:
    results = search_documents(query=query, top_k=top_k)
    return DocumentSearchResponse(query=query, top_k=top_k, results=results)
