from typing import Annotated
from pydantic import BaseModel, Field

PodcastEpisodeName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=50,
        title="Podcast Episode Name",
        description="Name of the item, between 3 and 50 characters",
    ),
]

PodcastEpisodeDescription = Annotated[
    str,
    Field(
        min_length=5,
        max_length=50,
        title="Description",
        description="Original description of the podcast episode",
    ),
]

GPTDescription = Annotated[
    str,
    Field(
        min_length=5,
        max_length=50,
        title="GPT Description",
        description="Description enhanced by GPT-4",
    ),
]


class PodcastEpisode(BaseModel):
    title: PodcastEpisodeName
    description: PodcastEpisodeDescription
    host: GPTDescription

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Future of AI",
                    "description": "We discuss upcoming trends in artificial intelligence.",
                    "host": "Joe Rogan",
                }
            ]
        }
    }


class PodcastEpisodeCreate(PodcastEpisode):
    pass


class PodcastEpisodeRead(PodcastEpisode):
    id: int


class PodcastEpisodeUpdate(PodcastEpisode):
    pass


class PodcastEpisodeDelete(BaseModel):
    id: int
