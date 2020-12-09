FROM python:3.8-slim AS base

LABEL version="1.0" maintainer="Alejandro Menor <alex4menor@gmail.com>"

WORKDIR que-vemos
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt update && \
    apt install -y --no-install-recommends build-essential

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY app app

CMD ["poetry", "run", "task", "start"]
