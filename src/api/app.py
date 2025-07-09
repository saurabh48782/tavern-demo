from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import customers, items


@asynccontextmanager
# pylint: disable=unused-argument
async def lifespan(appl: FastAPI):
    yield


app = FastAPI(title="Tavern Demo", lifespan=lifespan)


@app.get("/healthcheck", tags=['System status'])
async def healthcheck():
    return "Healthy!!"


@app.get("/", tags=['Homepage'])
async def home():
    return "Service is running. Use /docs for API documentation."


app.include_router(customers.router)
app.include_router(items.router)
