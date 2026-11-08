"""Explicit selection of one knowledge snapshot for the running process."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Mode = Literal["demo", "verified"]
Backend = Literal["json", "postgres"]
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AppConfig:
    mode: Mode
    data_root: Path
    knowledge_path: Path
    backend: Backend = "json"
    database_url: str | None = None
    knowledge_version: str | None = None


def read_config() -> AppConfig:
    """Read mode once; an unavailable verified file never falls back to demo."""
    raw_mode = os.environ.get("KNOWLEDGE_MODE", "demo")
    if raw_mode not in ("demo", "verified"):
        raise ValueError("KNOWLEDGE_MODE must be demo or verified")
    mode: Mode = raw_mode
    data_root = PROJECT_ROOT / "data"
    filename = "knowledge_demo.json" if mode == "demo" else "knowledge_verified.json"
    backend = os.environ.get("KNOWLEDGE_BACKEND", "json")
    if backend not in ("json", "postgres"):
        raise ValueError("KNOWLEDGE_BACKEND must be json or postgres")
    database_url = os.environ.get("DATABASE_URL") if backend == "postgres" else None
    version = os.environ.get("KNOWLEDGE_VERSION") if backend == "postgres" else None
    if backend == "postgres" and (mode != "verified" or not database_url or not version):
        raise ValueError("Postgres requires verified mode, DATABASE_URL and KNOWLEDGE_VERSION")
    return AppConfig(
        mode=mode,
        data_root=data_root,
        knowledge_path=data_root / mode / filename,
        backend=backend,
        database_url=database_url,
        knowledge_version=version,
    )
