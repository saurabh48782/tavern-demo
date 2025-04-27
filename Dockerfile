FROM python:3.10.13 AS python_base

RUN pip install poetry
COPY ./poetry.lock pyproject.toml /code/
WORKDIR /code

FROM python_base AS api_base
RUN poetry install --no-cache --no-root
COPY . /code/

FROM python_base AS api_base_test
RUN poetry install --no-cache --no-root --with dev
COPY ./.pre-commit-config.yaml /code/
RUN git init && poetry run pre-commit install-hooks
COPY . /code/

FROM api_base AS test_api
CMD scripts/start-api.sh

FROM api_base_test AS precommit_check
CMD scripts/precommit_check.sh

FROM api_base_test AS integration_test
CMD scripts/integration_test.sh
