from contextlib import asynccontextmanager, contextmanager
from typing import Annotated

import asyncpg
import psycopg2
from fastapi import Depends

from config import config

db_data = {}


@asynccontextmanager
async def db_lifespan():
    db_data['pool'] = await asyncpg.create_pool(config['db']['url'],
                                                min_size=1,
                                                max_size=10)
    yield
    await db_data['pool'].close()


@asynccontextmanager
async def db_conn(min_size=1, max_size=10):
    if config['db']['use_pool_outside_fastapi']:
        if 'pool' not in db_data:
            db_data['pool'] = await asyncpg.create_pool(config['db']['url'],
                                                        min_size=min_size,
                                                        max_size=max_size)
        async with db_data['pool'].acquire() as con:
            yield con
    else:
        # This case is used during integration testing. Otherwise there is an
        # issue with the pool becoming stale in a different event loop after
        # each test.
        async with connection() as con:
            yield con


@contextmanager
def sync_db_conn():
    conn = psycopg2.connect(config['db']['url'])
    try:
        yield conn
    finally:
        conn.close()


def db_pool():
    return db_data['pool']


@asynccontextmanager
async def connection():
    """Get a connection outside of the pool."""
    conn = await asyncpg.connect(config['db']['url'])
    try:
        yield conn
    except GeneratorExit:
        conn.close()


DBPool = Annotated[asyncpg.Pool, Depends(db_pool)]
