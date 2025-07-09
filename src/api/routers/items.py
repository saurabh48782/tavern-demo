from fastapi import APIRouter, HTTPException

from db import db_conn
from src.data.items import (Item, ItemWithId, add_item, delete_item,
                            get_item_info, list_items)

router = APIRouter(prefix="/item", tags=["Product Items"])


@router.put("/{item_id}", summary="Add an item.", status_code=201)
async def add_items(item_id: int, item: Item):
    item_data = ItemWithId(id=item_id, **item.model_dump())
    async with db_conn() as con:
        await add_item(con, item_data)
    return {"message": "Item added successfully."}


@router.get("/{item_id}", summary='Get item info.', response_model=Item)
async def get_item(item_id: int):
    async with db_conn() as con:
        item = await get_item_info(con, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(**item)


@router.get("/", summary='List all items.', response_model=list[ItemWithId])
async def list_all_items():
    async with db_conn() as con:
        return await list_items(con)


@router.delete("/{item_id}", summary="Remove an item.", status_code=200)
async def delete_items(item_id: int):
    async with db_conn() as con:
        await delete_item(con, item_id)
