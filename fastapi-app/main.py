from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.api.api_endpoints import router as podcasts_router
from app.ai_ollama.services.health_check import router as health_router
from app.ai_ollama.llm_api import router as llm_router
from core.config import settings
from core.models.db_helper import db_helper
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(podcasts_router, prefix=settings.api.prefix)
main_app.include_router(health_router)
main_app.include_router(llm_router)


@main_app.get("/")
def home():
    return {"msg": "Keep pushing :) "}


if __name__ == "__main__":
    print("LLM model loaded from env:", settings.llm.model)
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
