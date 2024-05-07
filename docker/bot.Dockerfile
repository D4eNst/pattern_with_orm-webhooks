FROM python:3.11.9-slim-bookworm as base

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
ENV POSTGRES_HOST=${POSTGRES_HOST:-db} \
    POSTGRES_PORT=${POSTGRES_PORT:-5432}

RUN apt-get update -q -y \
    && apt-get install -q -y netcat-traditional

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY docker/scripts /scripts
RUN chmod 755 /scripts/ -R
ENTRYPOINT ["/scripts/entrypoint.sh"]

COPY src .
