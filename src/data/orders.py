from datetime import datetime
from typing import List

from pydantic import BaseModel


class Order(BaseModel):
    customer_id: int
    item_ids: List[int]


class OrderWithId(Order):
    id: int
    created_at: datetime


async def create_order(con, order: Order):
    pass
