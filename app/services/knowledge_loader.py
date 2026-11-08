"""Explicit, fail-closed JSON knowledge loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import ValidationError

from app.schemas.knowledge import KnowledgeBase


class KnowledgeLoadError(ValueError):
    """The selected snapshot cannot be safely loaded."""


DEFAULT_DATA_ROOT = Path(__file__).resolve().parents[2] / "data"


def load_knowledge(
    path: Path,
    *,
    expected_mode: Literal["demo", "verified"],
    data_root: Path = DEFAULT_DATA_ROOT,
) -> KnowledgeBase:
    """Load only a file under the explicitly selected mode directory.

    `data_root` can be replaced by a temporary root in tests. No fallback occurs.
    """
    if expected_mode not in ("demo", "verified"):
        raise KnowledgeLoadError("invalid knowledge mode")
    selected_dir = (data_root / expected_mode).resolve()
    selected_path = Path(path).resolve()
    if not selected_path.is_relative_to(selected_dir) or not selected_path.is_file():
        raise KnowledgeLoadError("knowledge file missing or outside selected mode")
    try:
        with selected_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        knowledge = KnowledgeBase.model_validate(payload)
    except (OSError, UnicodeError, ValueError, ValidationError) as exc:
        raise KnowledgeLoadError("invalid knowledge snapshot") from exc
    if knowledge.mode != expected_mode:
        raise KnowledgeLoadError("knowledge mode does not match selected mode")
    return knowledge
