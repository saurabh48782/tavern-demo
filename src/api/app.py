from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import customers


@asynccontextmanager
# pylint: disable=unused-argument
async def lifespan(appl: FastAPI):
    yield


app = FastAPI(title="Tavern Demo", lifespan=lifespan)


@app.get("/healthcheck", tags=['System status'])
async def healthcheck():
    return ""


app.include_router(customers.router)
