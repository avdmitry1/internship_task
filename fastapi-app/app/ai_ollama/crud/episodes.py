from sqlalchemy.ext.asyncio import AsyncSession
from core.models.episode import Episode


async def get_episode_by_id(session: AsyncSession, episode_id: int):
    return await session.get(Episode, episode_id)
