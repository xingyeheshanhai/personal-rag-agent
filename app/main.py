from fastapi import FastAPI

from app.api.v1_router import api_v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Backend scaffold for a personal knowledge base RAG Agent.",
    )

    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    app.include_router(api_v1_router)

    return app


app = create_app()
