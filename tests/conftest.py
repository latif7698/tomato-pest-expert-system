"""Reusable synthetic knowledge fixture."""

import json
from pathlib import Path

import pytest

from app.services.knowledge_loader import load_knowledge

SAMPLE_PATH = Path(__file__).parent / "fixtures" / "knowledge_sample.json"


@pytest.fixture
def sample_payload() -> dict:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def sample_knowledge(tmp_path: Path, sample_payload: dict):
    demo_dir = tmp_path / "demo"
    demo_dir.mkdir()
    path = demo_dir / "knowledge.json"
    path.write_text(json.dumps(sample_payload), encoding="utf-8")
    return load_knowledge(path, expected_mode="demo", data_root=tmp_path)
