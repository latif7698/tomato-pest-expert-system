"""Integrity and mode isolation for JSON snapshots."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from app.services.knowledge_loader import KnowledgeLoadError, load_knowledge


def write_snapshot(root: Path, mode: str, payload: dict) -> Path:
    directory = root / mode
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "knowledge.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_loads_synthetic_fixture_with_mode_and_version(sample_knowledge):
    assert sample_knowledge.mode == "demo"
    assert sample_knowledge.knowledge_version == "demo-001"
    assert sample_knowledge.rules[0].validation_status == "synthetic"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data["pests"].append(deepcopy(data["pests"][0])),
        lambda data: data["symptoms"].append(deepcopy(data["symptoms"][0])),
        lambda data: data["sources"].append(deepcopy(data["sources"][0])),
        lambda data: data["rules"].append(deepcopy(data["rules"][0])),
        lambda data: data["rules"][0].update(pest_id="missing"),
        lambda data: data["rules"][0].update(symptom_id="missing"),
        lambda data: data["rules"][0].update(source_id="missing"),
        lambda data: data["pests"][0].update(source_ids=["missing"]),
        lambda data: data["symptoms"][0].update(source_ids=["missing"]),
        lambda data: data["rules"][0].update(validation_status="verified"),
        lambda data: data["sources"][0].update(access_status="reviewed"),
        lambda data: data["sources"][0].update(url="javascript:alert(1)"),
        lambda data: data["rules"][0].update(source_locator=" "),
        lambda data: data.update(knowledge_version=" "),
        lambda data: data.update(domain="tomato_diseases"),
        lambda data: data["pests"][0].update(handling="rekomendasi palsu"),
        lambda data: data.update(unexpected="forbidden"),
    ],
)
def test_rejects_invalid_knowledge(tmp_path, sample_payload, mutate):
    mutate(sample_payload)
    path = write_snapshot(tmp_path, "demo", sample_payload)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="demo", data_root=tmp_path)


@pytest.mark.parametrize(
    "value", [-0.1, 1.1, float("nan"), float("inf"), True, "0.5", 10**400]
)
def test_rejects_invalid_expert_weight(tmp_path, sample_payload, value):
    sample_payload["rules"][0]["cf_expert"] = value
    path = write_snapshot(tmp_path, "demo", sample_payload)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="demo", data_root=tmp_path)


def test_does_not_fallback_from_verified_to_demo(tmp_path, sample_payload):
    path = write_snapshot(tmp_path, "demo", sample_payload)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="verified", data_root=tmp_path)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(tmp_path / "verified" / "knowledge.json", expected_mode="verified", data_root=tmp_path)


def test_rejects_mode_mismatch_even_in_selected_directory(tmp_path, sample_payload):
    path = write_snapshot(tmp_path, "verified", sample_payload)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="verified", data_root=tmp_path)


def test_rejects_malformed_json(tmp_path):
    directory = tmp_path / "demo"
    directory.mkdir()
    path = directory / "knowledge.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="demo", data_root=tmp_path)


def test_rejects_path_outside_selected_data_root(tmp_path, sample_payload):
    other_root = tmp_path / "other"
    path = write_snapshot(other_root, "demo", sample_payload)
    with pytest.raises(KnowledgeLoadError):
        load_knowledge(path, expected_mode="demo", data_root=tmp_path)
