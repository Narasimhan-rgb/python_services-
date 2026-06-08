from datetime import datetime

from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "success": True,
        "service": "AAQ Python FastAPI Service",
        "status": "UP",
        "message": "Python service is healthy",
        "timestamp": datetime.now().isoformat()
    }