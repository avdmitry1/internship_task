from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from api.crud.crud import (
    create_podcast_db,
    delete_podcast_db,
    get_all_podcasts_db,
    get_podcast,
    update_podcast_db,
)
from core.schemas.podcast import (
    PodcastEpisodeRead,
    PodcastEpisodeCreate,
    PodcastEpisodeUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper

router = APIRouter(prefix="/episodes", tags=["Episodes"])


# curl -X 'GET' 'localhost:8000/api/episodes/'
@router.get("/", response_model=list[PodcastEpisodeRead])
async def read_all_episodes(
    session: AsyncSession = Depends(db_helper.get_session),
):
    episodes = await get_all_podcasts_db(session=session)
    return episodes or []


@router.get("/{episode_id}", response_model=PodcastEpisodeRead)
async def read_episode(
    episode_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    episode = await get_podcast(episode_id, session)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.post("/", response_model=PodcastEpisodeRead)
async def create_episode(
    episode: PodcastEpisodeCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    created_episode = await create_podcast_db(episode=episode, session=session)
    return created_episode


@router.put("/{episode_id}", response_model=PodcastEpisodeRead)
async def update_episode(
    episode: PodcastEpisodeUpdate,
    episode_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    updated_episode = await update_podcast_db(
        episode_id=episode_id,
        episode=episode,
        session=session,
    )
    if not updated_episode:
        raise HTTPException(status_code=400, detail="Item not updated")
    return updated_episode


@router.delete("/{episode_id}")
async def delete_item(
    episode_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    await delete_podcast_db(episode_id=episode_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
