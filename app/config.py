"""Explicit selection of one knowledge snapshot for the running process."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Mode = Literal["demo", "verified"]
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AppConfig:
    mode: Mode
    data_root: Path
    knowledge_path: Path


def read_config() -> AppConfig:
    """Read mode once; an unavailable verified file never falls back to demo."""
    raw_mode = os.environ.get("KNOWLEDGE_MODE", "demo")
    if raw_mode not in ("demo", "verified"):
        raise ValueError("KNOWLEDGE_MODE must be demo or verified")
    mode: Mode = raw_mode
    data_root = PROJECT_ROOT / "data"
    filename = "knowledge_demo.json" if mode == "demo" else "knowledge_verified.json"
    return AppConfig(mode=mode, data_root=data_root, knowledge_path=data_root / mode / filename)
