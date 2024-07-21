FROM python:3.11.9-slim-bookworm AS development_build

ARG BOT_ENV \
    # Needed for fixing permissions of files created by Docker:
    UID=1000 \
    GID=1000 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry:
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

ENV BOT_ENV=${BOT_ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# System deps
# hadolint ignore=DL3008
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        curl \
        netcat-traditional \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN groupadd -g "${GID}" -r bot \
    && useradd -d '/code' -g bot -l -r -u "${UID}" bot \
    && chown bot:bot -R '/code'

# Copy only requirements, to cache them in docker layer
COPY --chown=bot:bot ../poetry.lock ../pyproject.toml /code/

# Project initialization:
# hadolint ignore=SC2046
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
    echo "$BOT_ENV" \
    && poetry version \
    # Install deps:
    && poetry run pip install -U pip \
    && poetry install \
        $(if [ "$BOT_ENV" = 'production' ]; then echo '--only main'; fi) \
        --no-interaction --no-ansi --sync

COPY docker/scripts /scripts

# Setting up proper permissions:
RUN chmod +x /scripts/ -R \
    # Replacing line separator CRLF with LF for Windows users:
    && find /scripts -type f -exec sed -i 's/\r$//g' {} \;

USER bot

ENTRYPOINT ["/scripts/entrypoint.sh"]


# The following stage is only for production:
FROM development_build AS production_build
COPY --chown=bot:bot src .
