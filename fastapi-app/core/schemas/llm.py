from typing import Literal
from pydantic import BaseModel, Field


class GenAltRequest(BaseModel):
    # target -> either "title" or "description" (specify what you want the LLM to regenerate
    target: Literal["title", "description"]
    # prompt -> text instruction for the LLM
    prompt: str = Field(
        min_length=3,
        max_length=100,
        description="The prompt to generate alternatives for.",
        examples=[
            "Rewrite the description of this podcast",
            "Summarize this description for busy professionals",
            "Make the description more exciting and engaging",
        ],
    )


class GenAltResponse(BaseModel):
    original: dict[str, str] = Field(
        min_length=3,
        max_length=100,
        description="The original episode.",
    )
    target: str = Field(
        min_length=3,
        max_length=100,
        description="The target text.",
    )
    prompt: str = Field(
        min_length=3,
        max_length=100,
        description="The prompt.",
    )
    alternative: str = Field(
        min_length=1,
        max_length=100,
        description="The generated alternatives.",
    )
