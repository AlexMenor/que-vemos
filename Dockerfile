FROM python:3.8-slim AS base

LABEL version="1.0" maintainer="Alejandro Menor <alex4menor@gmail.com>" 

FROM base AS builder

RUN apt update && \
    apt install -y --no-install-recommends build-essential

RUN pip install poetry

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --dev | /venv/bin/pip install -r /dev/stdin

FROM base AS final

RUN groupadd -r tests && useradd --no-log-init -r -g tests tests

USER tests

ENV PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv

WORKDIR /test
VOLUME /test

CMD ["python", "-m", "pytest"]