from fastapi import APIRouter, HTTPException

from db import db_conn
from src.data.orders import Order, create_order

router = APIRouter(prefix="/order", tags=["Orders"])


@router.put("/", summary="Place an order.", status_code=201)
async def place_order(order: Order):
    try:
        async with db_conn() as con:
            order_id = await create_order(con, order)
            return {
                "message": "Order placed successfully",
                "order_id": order_id
            }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
