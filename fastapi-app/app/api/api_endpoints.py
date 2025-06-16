from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from app.api.crud.crud import (
    create_podcast_db,
    delete_podcast_db,
    get_all_podcasts_db,
    get_podcast,
    update_podcast_db,
)
from core.schemas.podcast import (
    PodcastRead,
    PodcastCreate,
    PodcastUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.get("/", response_model=list[PodcastRead])
async def read_all_podcasts(
    session: AsyncSession = Depends(db_helper.get_session),
) -> List[PodcastRead]:
    podcasts = await get_all_podcasts_db(session=session)
    return podcasts


@router.get("/{podcast_id}", response_model=PodcastRead)
async def read_podcast(
    podcast_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    podcast = await get_podcast(podcast_id, session)
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return podcast


@router.post("/", response_model=PodcastRead, status_code=status.HTTP_201_CREATED)
async def create_podcast(
    podcast: PodcastCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    try:
        created_podcast = await create_podcast_db(podcast=podcast, session=session)
        return created_podcast
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create podcast {e}")


@router.put("/{podcast_id}", response_model=PodcastRead)
async def update_podcast(
    podcast: PodcastUpdate,
    podcast_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    updated_podcast = await update_podcast_db(
        podcast_id=podcast_id,
        podcast=podcast,
        session=session,
    )
    if not updated_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return updated_podcast


@router.delete("/{podcast_id}")
async def delete_podcast(
    podcast_id: int = Path(gt=0),
    session: AsyncSession = Depends(db_helper.get_session),
):
    deleted_podcast = await delete_podcast_db(podcast_id=podcast_id, session=session)
    if not deleted_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
