"""
Health check router with cache statistics
"""
from fastapi import APIRouter
from app.services.cache_service import cache_service

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Sacha Advisor API",
        "cache": cache_service.get_stats()
    }
