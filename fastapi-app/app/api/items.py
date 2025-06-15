from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from .crud.items import (
    create_item_db,
    delete_item_db,
    get_all_items,
    get_item,
    update_item_db,
)
from core.schemas.item import ItemRead, ItemCreate, ItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper

router = APIRouter(prefix="/items", tags=["Items"])


# curl -X 'GET' 'localhost:8000/api/items/'
@router.get("/", response_model=list[ItemRead], status_code=status.HTTP_200_OK)
async def read_items(session: AsyncSession = Depends(db_helper.get_session)):
    items = await get_all_items(session=session)
    return items or []


# curl -X 'GET' 'localhost:8000/api/items/1'
@router.get("/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
async def read_item(
    item_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    item = await get_item(item_id, session)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    created_item = await create_item_db(item=item, session=session)
    return created_item


# curl -X 'PUT' 'localhost:8000/api/items/1'
@router.put("/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
async def update_item(
    item: ItemUpdate,
    item_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    updated_item = await update_item_db(item_id=item_id, item=item, session=session)
    if not updated_item:
        raise HTTPException(status_code=400, detail="Item not updated")
    return updated_item


# curl -X 'DELETE' 'localhost:8000/api/items/1'
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    await delete_item_db(item_id=item_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
