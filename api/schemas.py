from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    body: str


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
