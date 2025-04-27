import subprocess

import pytest

from config import config


@pytest.fixture
def fresh_db():
    subprocess.run(["poetry", "run", "alembic", "downgrade", "base"],
                   check=True)
    subprocess.run(["poetry", "run", "alembic", "upgrade", "head"], check=True)
    config['db']['use_pool_outside_fastapi'] = False
