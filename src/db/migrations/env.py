import sys
from logging.config import fileConfig

import asyncio
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

sys.path = ["", ".."] + sys.path[1:]  # TODO: Fix it

from setting import settings  # noqa
from src.base.db.database import DBBaseModel  # noqa

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = DBBaseModel.metadata

fileConfig(config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool)
    connectable = AsyncEngine(create_engine(settings.DATABASE_URL, echo=True, future=True))
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
        # context.configure(connection=connection, target_metadata=target_metadata)
        # with context.begin_transaction():
        #     context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
