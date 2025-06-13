from sqlalchemy.ext.asyncio import AsyncSession
from core.models.item import Item
from sqlalchemy import select
from core.schemas.item import ItemCreate, ItemRead


async def get_all_items(session: AsyncSession):
    stmt = select(Item).order_by(Item.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_item(item_id: ItemRead, session: AsyncSession):
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_item_db(item: ItemCreate, session: AsyncSession):
    db_item = Item(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item
