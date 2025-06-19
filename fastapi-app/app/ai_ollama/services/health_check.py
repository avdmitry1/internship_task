from fastapi import APIRouter
from app.ai_ollama.services.llm_service import llm_services

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    llm_healthy = await llm_services.connect_check()

    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected?",
        "llm_service": llm_healthy,
    }
