"""Immutable, checked knowledge import and consultation writes."""

import hashlib
import json
from uuid import uuid4

from sqlalchemy import Engine, insert, select

from app.db import models
from app.schemas.consultation import ConsultationRequest, ConsultationResponse
from app.schemas.knowledge import KnowledgeBase


class SnapshotError(ValueError):
    """The selected snapshot is absent, changed, or invalid."""


def digest(knowledge: KnowledgeBase) -> str:
    payload = knowledge.model_dump(mode="json")
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def import_snapshot(engine: Engine, knowledge: KnowledgeBase) -> bool:
    """Import one reviewed snapshot atomically. Never replace an existing version."""
    if knowledge.mode != "verified":
        raise SnapshotError("only reviewed verified knowledge may be imported")
    version = knowledge.knowledge_version
    checksum = digest(knowledge)
    with engine.begin() as connection:
        existing = connection.execute(
            select(models.snapshots.c.sha256).where(models.snapshots.c.version == version)
        ).scalar_one_or_none()
        if existing is not None:
            if existing != checksum:
                raise SnapshotError("knowledge version already exists with different contents")
            return False
        connection.execute(
            insert(models.snapshots).values(version=version, mode="verified", sha256=checksum)
        )
        for table, items in (
            (models.sources, knowledge.sources),
            (models.pests, knowledge.pests),
            (models.symptoms, knowledge.symptoms),
            (models.rules, knowledge.rules),
        ):
            if items:
                connection.execute(
                    insert(table),
                    [
                        {**item.model_dump(mode="json"), "version": version, "ordinal": index}
                        for index, item in enumerate(items)
                    ],
                )
    return True


def load_snapshot(engine: Engine, version: str) -> KnowledgeBase:
    """Read an explicitly pinned version, validating integrity and original order."""
    with engine.connect() as connection:
        row = (
            connection.execute(
                select(models.snapshots).where(models.snapshots.c.version == version)
            )
            .mappings()
            .one_or_none()
        )
        if row is None or row["mode"] != "verified":
            raise SnapshotError("verified knowledge version unavailable")
        payload = {"knowledge_version": version, "domain": "tomato_pests", "mode": "verified"}
        for name, table in (
            ("sources", models.sources),
            ("pests", models.pests),
            ("symptoms", models.symptoms),
            ("rules", models.rules),
        ):
            records = connection.execute(
                select(table).where(table.c.version == version).order_by(table.c.ordinal)
            ).mappings()
            payload[name] = [
                {key: value for key, value in record.items() if key not in ("version", "ordinal")}
                for record in records
            ]
    try:
        knowledge = KnowledgeBase.model_validate(payload)
    except ValueError as exc:
        raise SnapshotError("invalid stored knowledge") from exc
    if digest(knowledge) != row["sha256"]:
        raise SnapshotError("stored knowledge digest mismatch")
    return knowledge


def save_consultation(
    engine: Engine, request: ConsultationRequest, response: ConsultationResponse
) -> None:
    """Save anonymous input and result without changing the existing API response."""
    with engine.begin() as connection:
        connection.execute(
            insert(models.consultations).values(
                id=str(uuid4()),
                version=response.knowledge_version,
                observations=[item.model_dump(mode="json") for item in request.observations],
                result=response.model_dump(mode="json"),
            )
        )
