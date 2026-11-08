"""Versioned reviewed knowledge and anonymous consultation records.

Revision ID: 0001_reviewed_knowledge
Revises:
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001_reviewed_knowledge"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "knowledge_snapshots",
        sa.Column("version", sa.String(100), primary_key=True),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("mode = 'verified'", name="snapshot_verified_only"),
    )
    op.create_table(
        "knowledge_sources",
        sa.Column(
            "version",
            sa.String(100),
            sa.ForeignKey("knowledge_snapshots.version"),
            primary_key=True,
        ),
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("access_status", sa.String(16), nullable=False),
    )
    op.create_table(
        "knowledge_pests",
        sa.Column(
            "version",
            sa.String(100),
            sa.ForeignKey("knowledge_snapshots.version"),
            primary_key=True,
        ),
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("handling", sa.Text()),
        sa.Column("source_ids", JSONB(), nullable=False),
    )
    op.create_table(
        "knowledge_symptoms",
        sa.Column(
            "version",
            sa.String(100),
            sa.ForeignKey("knowledge_snapshots.version"),
            primary_key=True,
        ),
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("source_ids", JSONB(), nullable=False),
    )
    op.create_table(
        "knowledge_rules",
        sa.Column(
            "version",
            sa.String(100),
            sa.ForeignKey("knowledge_snapshots.version"),
            primary_key=True,
        ),
        sa.Column("pest_id", sa.String(80), primary_key=True),
        sa.Column("symptom_id", sa.String(80), primary_key=True),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("cf_expert", sa.Float(), nullable=False),
        sa.Column("source_id", sa.String(80), nullable=False),
        sa.Column("source_locator", sa.Text(), nullable=False),
        sa.Column("validation_status", sa.String(16), nullable=False),
        sa.ForeignKeyConstraint(
            ["version", "pest_id"], ["knowledge_pests.version", "knowledge_pests.id"]
        ),
        sa.ForeignKeyConstraint(
            ["version", "symptom_id"], ["knowledge_symptoms.version", "knowledge_symptoms.id"]
        ),
        sa.ForeignKeyConstraint(
            ["version", "source_id"], ["knowledge_sources.version", "knowledge_sources.id"]
        ),
        sa.CheckConstraint("cf_expert >= 0 AND cf_expert <= 1", name="rule_cf_range"),
    )
    op.create_table(
        "consultations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "version", sa.String(100), sa.ForeignKey("knowledge_snapshots.version"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("observations", JSONB(), nullable=False),
        sa.Column("result", JSONB(), nullable=False),
    )


def downgrade() -> None:
    # A destructive downgrade would delete reviewed knowledge and consultation records.
    raise RuntimeError("Irreversible migration: restore from a controlled backup instead")
