from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    source_file: str
    page_number: int


class DocumentUploadResponse(BaseModel):
    doc_id: str
    file_name: str
    file_type: str
    file_size: int
    saved_path: str
    chunk_count: int
    chunks: list[DocumentChunk]
    status: str


class DocumentSearchResult(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    source_file: str
    page_number: int
    distance: float | None = None


class DocumentSearchResponse(BaseModel):
    query: str
    top_k: int
    results: list[DocumentSearchResult]
