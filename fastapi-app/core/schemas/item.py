from typing import Annotated
from pydantic import BaseModel, Field

ItemName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=50,
        title="Item Name",
        description="Name of the item, between 3 and 50 characters",
    ),
]

ItemDescription = Annotated[
    str,
    Field(
        min_length=5,
        max_length=50,
        title="Description",
        description="Original description of the item",
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


class ItemBase(BaseModel):
    item: ItemName
    description: ItemDescription
    remaked_description: GPTDescription

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Sample Item",
                    "description": "Original description",
                    "remaked_description": "Enhanced by GPT-4",
                }
            ]
        }
    }


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
