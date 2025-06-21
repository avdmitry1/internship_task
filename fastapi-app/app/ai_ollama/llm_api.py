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
    episode_id: int = Path(..., gt=0, description="ID of the episode"),
    data: GenAltRequest = Body(..., description="Request data for target and prompt"),
    session: AsyncSession = Depends(db_helper.get_session),
):
    # get episode from db
    episode = await get_episode_by_id(session, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # transform episode to Pydantic episode model
    episode_data = Episode.model_validate(episode)

    try:
        result = await llm_services.generate_alternatives(
            episode_data=episode_data,
            target=data.target,
            user_prompt=data.prompt,
        )
        return {
            "original_episode": {
                "id": episode_id,
                "title": episode_data.title,
                "description": episode_data.description,
                "host": episode_data.host,
            },
            "request": {  # Group request data
                "target": data.target,
                "prompt": data.prompt,
            },
            "generated_alternative": result,
            "success": True,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating alternative: {e}",
        )
