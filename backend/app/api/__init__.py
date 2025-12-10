from fastapi import APIRouter

from app.api.routes import cover_letter, health


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(cover_letter.router, tags=["cover-letter"])
