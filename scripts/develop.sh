#!/bin/bash

set -ex
docker compose --profile dev up --build -d --wait

export ENVIRONMENT_VARIABLES=$(cat <<EOF
{
"db.url": "postgresql://test_user:test_password@localhost/ecommerce",
"api.url": "http://localhost:8000"
}
EOF
)

poetry run alembic upgrade head
poetry run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

docker compose --profile dev down
