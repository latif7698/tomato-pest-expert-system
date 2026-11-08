"""Explicit import: python -m app.db.seed (after alembic upgrade head)."""

import os

from sqlalchemy import create_engine

from app.config import PROJECT_ROOT
from app.db.store import import_snapshot
from app.services.knowledge_loader import load_knowledge


def main() -> None:
    url = os.environ.get("DATABASE_DIRECT_URL")
    if not url or not url.startswith("postgresql+psycopg://"):
        raise ValueError("DATABASE_DIRECT_URL must be a direct postgresql+psycopg URL")
    data_root = PROJECT_ROOT / "data"
    knowledge = load_knowledge(
        data_root / "verified" / "knowledge_verified.json",
        expected_mode="verified",
        data_root=data_root,
    )
    engine = create_engine(url, pool_pre_ping=True)
    try:
        changed = import_snapshot(engine, knowledge)
        print(
            f"Snapshot {knowledge.knowledge_version}: {'imported' if changed else 'already present'}"
        )
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
