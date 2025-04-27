#!/bin/bash

mkdir -p logs
poetry run pytest -vv tests/integration
