from typing import Literal
from pydantic import BaseModel, Field


class Episode(BaseModel):
    id: int
    title: str
    description: str
    host: str

    model_config = {"from_attributes": True}


class GenAltRequest(BaseModel):
    target: Literal["title", "description"]
    prompt: str


class GenAltResponse(BaseModel):
    original: Episode = Field(alias="originalEpisode")
    target: Literal["title", "description"]
    prompt: str
    alternative: str

    # for more validation
    model_config = {"validate_by_name": True}
