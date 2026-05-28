import hashlib
import math
import re

from app.database.chroma import get_default_collection
from app.schemas.document import DocumentChunk, DocumentSearchResult


EMBEDDING_DIMENSIONS = 384


def embed_texts(texts: list[str]) -> list[list[float]]:
    return [_embed_text(text) for text in texts]


def add_document_chunks(chunks: list[DocumentChunk]) -> None:
    if not chunks:
        return

    collection = get_default_collection()
    collection.upsert(
        ids=[chunk.chunk_id for chunk in chunks],
        embeddings=embed_texts([chunk.text for chunk in chunks]),
        documents=[chunk.text for chunk in chunks],
        metadatas=[
            {
                "doc_id": chunk.doc_id,
                "source_file": chunk.source_file,
                "page_number": chunk.page_number,
            }
            for chunk in chunks
        ],
    )


def search_documents(query: str, top_k: int = 5) -> list[DocumentSearchResult]:
    normalized_query = query.strip()
    if not normalized_query:
        return []

    collection = get_default_collection()
    if collection.count() == 0:
        return []

    result = collection.query(
        query_embeddings=embed_texts([normalized_query]),
        n_results=max(1, top_k),
        include=["documents", "metadatas", "distances"],
    )

    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    search_results: list[DocumentSearchResult] = []
    for index, chunk_id in enumerate(ids):
        metadata = metadatas[index] or {}
        search_results.append(
            DocumentSearchResult(
                chunk_id=chunk_id,
                doc_id=str(metadata.get("doc_id", "")),
                text=documents[index] or "",
                source_file=str(metadata.get("source_file", "")),
                page_number=int(metadata.get("page_number", 0)),
                distance=distances[index] if index < len(distances) else None,
            )
        )

    return search_results


def _embed_text(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSIONS
    tokens = _tokenize(text)

    for token in tokens:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, byteorder="big", signed=False)
        index = value % EMBEDDING_DIMENSIONS
        sign = 1.0 if value & 1 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector

    return [value / norm for value in vector]


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\w+", text.lower())
    if tokens:
        return tokens

    return [char for char in text.strip() if not char.isspace()]
