"""Integration check against the disposable PostgreSQL service in CI."""

import os

import pytest
from sqlalchemy import create_engine, func, select
from test_database import post

from app.config import PROJECT_ROOT, AppConfig
from app.db.models import consultations
from app.db.store import load_snapshot
from app.main import create_app


def test_postgres_import_and_consultation():
    url = os.environ.get("TEST_DATABASE_DIRECT_URL")
    if not url:
        pytest.skip("requires the isolated CI PostgreSQL service")
    engine = create_engine(url)
    try:
        knowledge = load_snapshot(engine, "l04-2026-11-08-v1")
        assert (len(knowledge.pests), len(knowledge.symptoms), len(knowledge.rules)) == (5, 10, 11)
        app = create_app(
            AppConfig(
                mode="verified",
                data_root=PROJECT_ROOT / "data",
                knowledge_path=PROJECT_ROOT / "data/verified/knowledge_verified.json",
                backend="postgres",
                database_url=url,
                knowledge_version=knowledge.knowledge_version,
                persist_consultations=True,
            ),
            engine=engine,
        )
        response = post(
            app, {"observations": [{"symptom_id": knowledge.rules[0].symptom_id, "cf_user": 1.0}]}
        )
        assert response.status_code == 200
        assert response.json()["mode"] == "verified"
        with engine.connect() as connection:
            assert connection.scalar(select(func.count()).select_from(consultations)) >= 1
    finally:
        engine.dispose()
