from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# IMPORT BASE & MODELS
# -------------------------------------------------
from app.models.base import Base
import app.models  # IMPORTANT: registers User, Student, etc.

target_metadata = Base.metadata

# -------------------------------------------------
# DATABASE URL - Convert async to sync for Alembic
# -------------------------------------------------
# Alembic works with sync connections, so we convert asyncpg to psycopg2
DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:1234@localhost/Ofc"
DATABASE_URL = DATABASE_URL_ASYNC.replace("postgresql+asyncpg", "postgresql")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# -------------------------------------------------
# OFFLINE MIGRATIONS
# -------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# -------------------------------------------------
# ONLINE MIGRATIONS (SYNC)
# -------------------------------------------------
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL,
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

# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
