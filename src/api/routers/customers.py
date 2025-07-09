from fastapi import APIRouter, Depends, HTTPException

from db import db_conn
from src.data.customers import (Customer, CustomerWithId, delete_customer_info,
                                get_customer_info, put_customer)

router = APIRouter(prefix="/customer", tags=["Customers"])


@router.put("/{identifier}", summary="Register a customer.", status_code=201)
async def add_customer(identifier: int, customer: Customer = Depends()):
    try:
        async with db_conn() as con:
            await put_customer(con, identifier, customer.name, customer.email)
        return {"message": "Customer registered successfully."}
    except Exception as e:
        raise e


@router.get("/{identifier}",
            summary="Customer information by identifier.",
            response_model=CustomerWithId)
async def get_customers(identifier: int) -> CustomerWithId:
    async with db_conn() as con:
        customer_data = await get_customer_info(con, identifier)
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found.")
        return CustomerWithId(id=customer_data['id'],
                              name=customer_data['name'],
                              email=customer_data['email'])


@router.delete("/{identifier}", summary="Remove a customer.", status_code=200)
async def delete_customer(identifier: int):
    async with db_conn() as con:
        await delete_customer_info(con, identifier)
