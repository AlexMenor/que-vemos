FROM python:3.8-slim AS base

LABEL version="1.0" maintainer="Alejandro Menor <alex4menor@gmail.com>"

RUN apt update && \
    apt install -y --no-install-recommends build-essential

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY app app

CMD ["poetry", "run", "task", "start"]
