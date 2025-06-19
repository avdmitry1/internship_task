from fastapi import APIRouter, HTTPException, Path, Body, Depends
from core.schemas.llmSchema import GenAltRequest
from app.ai_ollama.services.llm_service import llm_services
from core.schemas.llmSchema import Episode
from app.ai_ollama.crud.episodes import get_episode_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper


router = APIRouter(prefix="/episodes", tags=["Episodes"])


@router.post("/{episode_id}/generate_alternative")
async def generate_alternative(
    episode_id: int = Path(...),
    data: GenAltRequest = Body(...),
    session: AsyncSession = Depends(db_helper.get_session),
):
    episode = await get_episode_by_id(session, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # Преобразуем episode в Pydantic-модель (если нужно)
    episode_data = Episode.model_validate(episode)

    req = GenAltRequest(
        target=data.target,
        prompt=data.prompt,
    )

    try:
        result = await llm_services.generate_alternatives(
            podcast=req,
            target=data.target,
            user_prompt=data.prompt,
            episode_data=episode_data,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return {
        "original_episode": {
            "title": episode_data.title,
            "description": episode_data.description,
            "host": episode_data.host,
        },
        "target": data.target,
        "prompt": data.prompt,
        "generated_alternative": result,
    }
