"""Storage contract tests with an isolated SQL database; no Neon credentials needed."""

import asyncio
from pathlib import Path

import httpx
import pytest
from sqlalchemy import create_engine, func, select, update
from sqlalchemy.exc import OperationalError

from app.config import PROJECT_ROOT, AppConfig, read_config
from app.db.models import consultations, metadata, snapshots
from app.db.store import SnapshotError, import_snapshot, load_snapshot
from app.main import create_app
from app.services.knowledge_loader import load_knowledge


@pytest.fixture
def engine(tmp_path):
    instance = create_engine(f"sqlite:///{tmp_path / 'database.sqlite'}")
    metadata.create_all(instance)
    yield instance
    instance.dispose()


@pytest.fixture
def verified():
    root = PROJECT_ROOT / "data"
    return load_knowledge(
        root / "verified" / "knowledge_verified.json", expected_mode="verified", data_root=root
    )


def db_app(engine, knowledge, *, persist_consultations=False):
    config = AppConfig(
        mode="verified",
        data_root=Path("unused"),
        knowledge_path=Path("unused"),
        backend="postgres",
        knowledge_version=knowledge.knowledge_version,
        persist_consultations=persist_consultations,
    )
    return create_app(config, engine=engine)


def request_app(app, method, path, payload=None):
    async def perform():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.request(method, path, json=payload)

    return asyncio.run(perform())


def post(app, payload):
    return request_app(app, "POST", "/consultations", payload)


def test_import_is_idempotent_and_preserves_cf_and_source_order(engine, verified):
    assert import_snapshot(engine, verified)
    assert not import_snapshot(engine, verified)
    assert load_snapshot(engine, verified.knowledge_version) == verified
    with engine.connect() as connection:
        assert connection.scalar(select(func.count()).select_from(snapshots)) == 1


def test_import_rejects_reuse_of_version_and_demo(engine, verified, sample_knowledge):
    with pytest.raises(SnapshotError):
        import_snapshot(engine, sample_knowledge)
    import_snapshot(engine, verified)
    altered = verified.model_copy(
        update={
            "pests": [
                verified.pests[0].model_copy(update={"description": "Changed"}),
                *verified.pests[1:],
            ]
        }
    )
    with pytest.raises(SnapshotError, match="different contents"):
        import_snapshot(engine, altered)
    assert load_snapshot(engine, verified.knowledge_version) == verified


def test_missing_or_modified_snapshot_fails_closed(engine, verified):
    with pytest.raises(SnapshotError, match="unavailable"):
        db_app(engine, verified)
    import_snapshot(engine, verified)
    with engine.begin() as connection:
        connection.execute(update(snapshots).values(sha256="0" * 64))
    with pytest.raises(SnapshotError, match="digest mismatch"):
        db_app(engine, verified)


def test_database_consultation_matches_json_and_persists_anonymously(engine, verified):
    import_snapshot(engine, verified)
    observations = [{"symptom_id": verified.rules[0].symptom_id, "cf_user": 1.0}]
    db_response = post(
        db_app(engine, verified, persist_consultations=True), {"observations": observations}
    )
    json_app = create_app(
        AppConfig(
            mode="verified",
            data_root=PROJECT_ROOT / "data",
            knowledge_path=PROJECT_ROOT / "data/verified/knowledge_verified.json",
        )
    )
    json_response = post(json_app, {"observations": observations})
    assert db_response.status_code == 200
    assert db_response.json() == json_response.json()
    for path in ("/symptoms", f"/pests/{verified.pests[0].id}"):
        assert (
            request_app(db_app(engine, verified), "GET", path).json()
            == request_app(json_app, "GET", path).json()
        )
    assert request_app(db_app(engine, verified), "GET", "/healthz").json() == {"status": "ok"}
    with engine.connect() as connection:
        rows = connection.execute(select(consultations)).mappings().all()
    assert len(rows) == 1
    assert rows[0]["version"] == verified.knowledge_version
    assert rows[0]["observations"] == observations
    assert rows[0]["result"] == db_response.json()
    assert "user_id" not in rows[0] and "ip_address" not in rows[0]


def test_no_support_is_recorded_and_invalid_input_is_not(engine, verified):
    import_snapshot(engine, verified)
    app = db_app(engine, verified, persist_consultations=True)
    assert post(app, {"observations": []}).json()["status"] == "no_support"
    assert post(app, {"observations": [{"symptom_id": "bad", "cf_user": 1}]}).status_code == 422
    with engine.connect() as connection:
        assert connection.scalar(select(func.count()).select_from(consultations)) == 1


def test_failed_write_reports_503_without_false_success(engine, verified):
    import_snapshot(engine, verified)
    app = db_app(engine, verified, persist_consultations=True)
    with engine.begin() as connection:
        consultations.drop(connection)
    response = post(app, {"observations": []})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "storage_unavailable"
    assert "database.sqlite" not in response.text


def test_failed_health_reports_503(engine, verified):
    import_snapshot(engine, verified)
    app = db_app(engine, verified)

    class DownDatabase:
        def connect(self):
            raise OperationalError("SELECT 1", {}, Exception("unavailable"))

    app.state.db_engine = DownDatabase()
    response = request_app(app, "GET", "/healthz")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "storage_unavailable"


def test_database_consultation_does_not_store_history_by_default(engine, verified):
    import_snapshot(engine, verified)
    app = db_app(engine, verified)
    assert post(app, {"observations": []}).status_code == 200
    with engine.connect() as connection:
        assert connection.scalar(select(func.count()).select_from(consultations)) == 0


def test_persistence_requires_explicit_postgres_mode(monkeypatch):
    monkeypatch.setenv("PERSIST_CONSULTATIONS", "true")
    monkeypatch.setenv("KNOWLEDGE_BACKEND", "json")
    with pytest.raises(ValueError, match="requires postgres"):
        read_config()
    monkeypatch.setenv("PERSIST_CONSULTATIONS", "yes")
    with pytest.raises(ValueError, match="must be true or false"):
        read_config()


def test_config_requires_explicit_database_mode(monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_BACKEND", "postgres")
    monkeypatch.setenv("KNOWLEDGE_MODE", "verified")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValueError, match="DATABASE_URL"):
        read_config()
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://example/db")
    monkeypatch.setenv("KNOWLEDGE_VERSION", "l04-2026-11-08-v1")
    assert read_config().backend == "postgres"
