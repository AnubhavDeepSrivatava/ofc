from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

from app.core.config import settings
from app.models.base import Base

# IMPORTANT: Import ALL models so metadata is populated
from app.models.users import User
from app.models.student import Student

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the key line Alembic uses for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = str(settings.SQLALCHEMY_DATABASE_URI).replace(
        "postgresql+asyncpg",
        "postgresql"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    database_url = str(settings.SQLALCHEMY_DATABASE_URI).replace(
        "postgresql+asyncpg",
        "postgresql"
    )

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
