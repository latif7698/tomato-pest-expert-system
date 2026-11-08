"""Run migrations with a direct Neon connection, never the pooled app URL."""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from app.db.models import metadata

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata = metadata


def run_migrations_online() -> None:
    url = os.environ.get("DATABASE_DIRECT_URL")
    if not url or not url.startswith("postgresql+psycopg://"):
        raise ValueError("DATABASE_DIRECT_URL must be a direct postgresql+psycopg URL")
    engine = create_engine(url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


run_migrations_online()
