from pathlib import Path

from app.schemas.document import DocumentChunk
from app.services.document_loader import load_document_pages
from app.services.text_splitter import split_text


def parse_document_to_chunks(
    file_path: str | Path,
    doc_id: str,
    source_file: str | None = None,
) -> list[DocumentChunk]:
    path = Path(file_path)
    source_name = source_file or path.name
    chunks: list[DocumentChunk] = []

    for page in load_document_pages(path):
        for text in split_text(page.text):
            if not text.strip():
                continue

            chunk_index = len(chunks) + 1
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{doc_id}-{chunk_index:06d}",
                    doc_id=doc_id,
                    text=text,
                    source_file=source_name,
                    page_number=page.page_number,
                )
            )

    return chunks
