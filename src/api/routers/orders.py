from fastapi import APIRouter

router = APIRouter(prefix="/order", tags=["Orders"])


@router.put("/{identifier}", summary="Register an order.", status_code=201)
async def put_order(id: int):
    pass
