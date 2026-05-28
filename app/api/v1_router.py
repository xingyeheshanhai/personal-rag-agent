from fastapi import APIRouter

from app.api.routes.health import router as health_router


api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["health"])
