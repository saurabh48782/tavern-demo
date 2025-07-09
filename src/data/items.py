from typing import List, Optional

from asyncpg import Connection
from pydantic import BaseModel, Field
from pypika import Query, Table


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    in_stock: bool = True


class ItemWithId(Item):
    id: int


async def add_item(con: Connection, item: ItemWithId):
    items = Table("items")
    q = Query.into(items).columns("id", "name",
                                  "description", "price", "in_stock") \
        .insert(item.id, item.name,
                item.description, item.price, item.in_stock)
    await con.execute(str(q))
    return {"message": "Item added successfully."}


async def get_item_info(con: Connection, item_id: int):
    item = Table("items")
    q = Query.from_(item).select('*')
    q = q.where(item.id == item_id)
    res = await con.fetchrow(str(q))

    return dict(res) if res else None


async def delete_item(con: Connection, item_id: int):
    item = Table("items")
    q = Query.from_(item)
    q = q.where(item.id == item_id)
    q = q.delete()
    await con.execute(str(q))


async def list_items(con: Connection) -> List[ItemWithId]:
    items = Table("items")
    q = Query.from_(items).select("*")
    rows = await con.fetch(str(q))
    return [ItemWithId(**dict(row)) for row in rows]
