from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "assistant": settings.JARVIS_NAME
    }
