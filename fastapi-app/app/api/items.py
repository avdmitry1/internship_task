from fastapi import APIRouter, Depends
from .crud.items import create_item_db, get_all_items
from core.schemas.item import ItemRead, ItemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemRead])
async def read_items(session: AsyncSession = Depends(db_helper.get_session)):
    items = await get_all_items(session=session)
    return items


@router.post("/", response_model=ItemCreate)
async def create_item(
    item: ItemCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    item = await create_item_db(item=item, session=session)
    return item
