import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings

from app.core.config import settings


def get_chroma_client() -> ClientAPI:
    return chromadb.PersistentClient(
        path=settings.chroma_persist_directory,
        settings=Settings(anonymized_telemetry=False),
    )


def get_default_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=settings.chroma_collection_name)
