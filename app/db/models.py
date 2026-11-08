"""Database schema; migrations are the only production schema writer."""

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()
document = JSON().with_variant(JSONB(), "postgresql")

snapshots = Table(
    "knowledge_snapshots",
    metadata,
    Column("version", String(100), primary_key=True),
    Column("mode", String(16), nullable=False),
    Column("sha256", String(64), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint("mode = 'verified'", name="snapshot_verified_only"),
)

sources = Table(
    "knowledge_sources",
    metadata,
    Column("version", String(100), ForeignKey("knowledge_snapshots.version"), primary_key=True),
    Column("id", String(80), primary_key=True),
    Column("ordinal", Integer, nullable=False),
    Column("title", Text, nullable=False),
    Column("url", Text, nullable=False),
    Column("access_status", String(16), nullable=False),
)

pests = Table(
    "knowledge_pests",
    metadata,
    Column("version", String(100), ForeignKey("knowledge_snapshots.version"), primary_key=True),
    Column("id", String(80), primary_key=True),
    Column("ordinal", Integer, nullable=False),
    Column("name", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("handling", Text),
    Column("source_ids", document, nullable=False),
)

symptoms = Table(
    "knowledge_symptoms",
    metadata,
    Column("version", String(100), ForeignKey("knowledge_snapshots.version"), primary_key=True),
    Column("id", String(80), primary_key=True),
    Column("ordinal", Integer, nullable=False),
    Column("label", Text, nullable=False),
    Column("source_ids", document, nullable=False),
)

rules = Table(
    "knowledge_rules",
    metadata,
    Column("version", String(100), ForeignKey("knowledge_snapshots.version"), primary_key=True),
    Column("pest_id", String(80), primary_key=True),
    Column("symptom_id", String(80), primary_key=True),
    Column("ordinal", Integer, nullable=False),
    Column("cf_expert", Float, nullable=False),
    Column("source_id", String(80), nullable=False),
    Column("source_locator", Text, nullable=False),
    Column("validation_status", String(16), nullable=False),
    ForeignKeyConstraint(["version", "pest_id"], ["knowledge_pests.version", "knowledge_pests.id"]),
    ForeignKeyConstraint(
        ["version", "symptom_id"], ["knowledge_symptoms.version", "knowledge_symptoms.id"]
    ),
    ForeignKeyConstraint(
        ["version", "source_id"], ["knowledge_sources.version", "knowledge_sources.id"]
    ),
    CheckConstraint("cf_expert >= 0 AND cf_expert <= 1", name="rule_cf_range"),
)

consultations = Table(
    "consultations",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("version", String(100), ForeignKey("knowledge_snapshots.version"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("observations", document, nullable=False),
    Column("result", document, nullable=False),
)
