from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    in_stock: bool = True


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
