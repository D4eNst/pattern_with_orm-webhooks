# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
ENV POSTGRES_HOST=${POSTGRES_HOST:-db} \
    POSTGRES_PORT=${POSTGRES_PORT:-5432}
#ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

RUN apt-get update -q -y \
    && apt-get install -q -y netcat

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker/scripts /scripts
RUN chmod 755 /scripts/ -R
ENTRYPOINT ["/scripts/entrypoint.sh"]

COPY . .
