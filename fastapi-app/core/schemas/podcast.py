from typing import Optional
from pydantic import BaseModel, Field


class Podcast(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=500)
    host: str = Field(min_length=2, max_length=100)


class PodcastCreate(Podcast):
    pass


class PodcastUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=3, max_length=500)
    host: Optional[str] = Field(None, min_length=2, max_length=100)


class PodcastRead(Podcast):
    id: int

    model_config = {"from_attributes": True}
