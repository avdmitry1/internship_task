from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.api.api_endpoints import router as podcasts_router
from core.config import settings
from core.models.db_helper import db_helper
from core.models.model_podcast import Podcast


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(podcasts_router, prefix=settings.api.prefix)


# curl "http://127.0.0.1:8000/"
@main_app.get("/")
def home():
    return {"msg": "Keep pushing :)"}


if __name__ == "__main__":
    print(Podcast.__tablename__)
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
