from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    item: str = Field(
        min_length=3,
        max_length=50,
        title="The name of the item",
    )
    description: str = Field(
        min_length=5,
        max_length=50,
        title="The description of the item",
    )
    remaked_description: str = Field(
        min_length=5,
        max_length=50,
        title="The description of the item remaked by GPT4",
    )


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
