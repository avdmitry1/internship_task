from sqlalchemy.ext.asyncio import AsyncSession
from core.models.model_podcast import Podcast
from sqlalchemy import select
from core.schemas.podcast import (
    PodcastCreate,
    PodcastUpdate,
)


async def get_all_podcasts_db(session: AsyncSession):
    stmt = select(Podcast).order_by(Podcast.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_podcast(
    podcast_id: int,
    session: AsyncSession,
):
    stmt = select(Podcast).where(Podcast.id == podcast_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_podcast_db(
    podcast: PodcastCreate,
    session: AsyncSession,
):
    db_podcast = Podcast(**podcast.model_dump())
    session.add(db_podcast)
    await session.commit()
    await session.refresh(db_podcast)
    return db_podcast


async def update_podcast_db(
    podcast_id: int,
    podcast: PodcastUpdate,
    session: AsyncSession,
):
    db_podcast = await get_podcast(podcast_id, session)
    if not db_podcast:
        return None
    for var, value in podcast.model_dump(exclude_unset=True).items():
        setattr(db_podcast, var, value)
    session.add(db_podcast)
    await session.commit()
    await session.refresh(db_podcast)
    return db_podcast


async def delete_podcast_db(
    podcast_id: int,
    session: AsyncSession,
):
    db_podcast = await get_podcast(podcast_id, session)
    if not db_podcast:
        return None
    await session.delete(db_podcast)
    await session.commit()
    return db_podcast
