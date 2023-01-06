FROM python:3.9-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

FROM base AS builder

WORKDIR /tmp

ENV POETRY_VERSION=1.3.0 

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM base as runtime

WORKDIR /code

COPY --from=builder /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini ./
COPY alembic alembic
COPY app app

EXPOSE 8000 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]