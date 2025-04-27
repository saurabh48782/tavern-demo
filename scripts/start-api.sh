#!/bin/bash

set -ex

poetry run alembic upgrade head
poetry run uvicorn src.api.app:app --host 0.0.0.0 --port 8000
