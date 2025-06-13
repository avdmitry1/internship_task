from fastapi import APIRouter, Depends, HTTPException, Path, status
from .crud.items import create_item_db, get_all_items, get_item
from core.schemas.item import ItemRead, ItemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemRead], status_code=status.HTTP_200_OK)
async def read_items(session: AsyncSession = Depends(db_helper.get_session)):
    items = await get_all_items(session=session)
    return items or []


@router.get("/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
async def read_item(
    item_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    item = await get_item(item_id, session)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemCreate, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    created_item = await create_item_db(item=item, session=session)
    if not create_item:
        raise HTTPException(status_code=400, detail="Item not created")
    return created_item
