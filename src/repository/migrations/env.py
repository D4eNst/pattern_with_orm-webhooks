import re
from logging.config import fileConfig

from alembic import context
from alembic.operations import MigrationScript
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from repository.database import async_db
from repository.models.base import Base

# import all models to alembic generate correct migrations
from repository.models import *  # type: ignore

config = context.config
config.set_main_option(name="sqlalchemy.url", value=f"{async_db.async_postgres_dsn}?async_fallback=True")
config.set_main_option('revision_environment', 'true')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def process_revision_directives(context: MigrationContext, revision: tuple[str], directives: list[MigrationScript]):
    if len(directives) > 0:
        current_head = context.script.get_current_head()
        script = directives[0]
        script.rev_id = get_next_revision_id(current_head)
        script.slug = re.sub(r'[^a-z0-9]+', '_', script.message.lower())
        script.path = f"{script.rev_id}_{script.slug}.py"


def get_next_revision_id(current_head: str | None):
    if current_head is None:
        return "0001"
    current_id = int(current_head[:4])
    return f"{current_id + 1:04d}"


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
