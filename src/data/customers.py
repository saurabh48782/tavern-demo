from asyncpg import Connection
from pydantic import BaseModel, EmailStr
from pypika import Query, Table


class Customer(BaseModel):
    name: str
    email: EmailStr


class CustomerWithId(Customer):
    id: int


async def put_customer(con: Connection, id: int, name: str, email: str):
    customer = Table("customers")
    q = Query.into(customer).columns("id", "name",
                                     "email").insert(id, name, email)
    await con.execute(str(q))

    return {"message": "Customer registered successfully."}


async def get_customer_info(con: Connection, customer_id: int):
    customer = Table("customers")
    q = Query.from_(customer).select('id', 'name', 'email')
    q = q.where(customer.id == customer_id)
    res = await con.fetchrow(str(q))
    if not res:
        return None
    return dict(res)
