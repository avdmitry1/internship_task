from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.api.items import router as items_router
from core.config import settings
from core.models.db_helper import db_helper
from core.models.item import Item


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(items_router, prefix=settings.api.prefix)


@main_app.get("/")
def home():
    return {"msg": "Keep pushing :)"}


if __name__ == "__main__":
    print(Item.__tablename__)
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
