from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderBase(BaseModel):
    customer_id: int
    item_ids: List[int]


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    created_at: datetime
