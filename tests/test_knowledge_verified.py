"""The human-reviewed L04 snapshot through loader, API, and CF flow."""

import asyncio
import json
from decimal import Decimal
from pathlib import Path

import httpx
import pytest

from app.config import AppConfig
from app.main import create_app
from app.services.knowledge_loader import KnowledgeLoadError, load_knowledge

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
VERIFIED_PATH = DATA_ROOT / "verified" / "knowledge_verified.json"
REVIEW_PATH = DATA_ROOT / "review" / "l04_extraction.json"
CANDIDATE_PATH = DATA_ROOT / "review" / "l04_candidate_knowledge.json"


def call(app, method: str, path: str, **kwargs) -> httpx.Response:
    async def perform() -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(perform())


def verified_app():
    config = AppConfig(mode="verified", data_root=DATA_ROOT, knowledge_path=VERIFIED_PATH)
    return create_app(config)


def test_verified_snapshot_matches_reviewed_relations():
    knowledge = load_knowledge(VERIFIED_PATH, expected_mode="verified", data_root=DATA_ROOT)
    extraction = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
    candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
    modeled = {
        (row["pest_code"], row["symptom_code"]): row
        for row in extraction["relations"]
        if row["mvp_option_b_disposition"] == "dimodelkan"
    }
    omitted = {
        (row["pest_code"], row["symptom_code"])
        for row in extraction["relations"]
        if row["mvp_option_b_disposition"] != "dimodelkan"
    }

    assert knowledge.mode == "verified"
    assert knowledge.knowledge_version == "l04-2026-11-08-v1"
    assert (len(knowledge.pests), len(knowledge.symptoms), len(knowledge.rules)) == (5, 10, 11)
    assert {pest.id for pest in knowledge.pests} == {"P9", "P10", "P12", "P13", "P14"}
    assert {source.id for source in knowledge.sources} == {
        "SRC-01", "SRC-02", "SRC-03", "SRC-05", "SRC-06", "SRC-07"
    }
    assert all(source.access_status == "reviewed" and source.url for source in knowledge.sources)
    assert all(rule.validation_status == "verified" for rule in knowledge.rules)
    assert all(pest.handling is None for pest in knowledge.pests)
    assert {pest.id: pest.description for pest in knowledge.pests} == {
        pest["id"]: pest["description"] for pest in candidate["pests"]
    }
    assert {pest.id: pest.source_ids for pest in knowledge.pests} == {
        pest["id"]: pest["source_ids"] for pest in candidate["pests"]
    }
    assert {symptom.id: symptom.label for symptom in knowledge.symptoms} == {
        symptom["id"]: symptom["label"] for symptom in candidate["symptoms"]
    }
    pairs = {(rule.pest_id, rule.symptom_id) for rule in knowledge.rules}
    assert pairs == set(modeled) and not pairs & omitted and len(omitted) == 8
    for rule in knowledge.rules:
        row = modeled[(rule.pest_id, rule.symptom_id)]
        cf = Decimal(str(row["mb_transcribed"])) - Decimal(str(row["md_transcribed"]))
        assert Decimal(str(rule.cf_expert)) == cf == Decimal(str(row["cf_expert_calc_mb_minus_md"]))
        assert rule.source_id == "SRC-01"
        assert f"hal. cetak {row['source']['printed_page']}" in rule.source_locator
        assert "Tabel IV" in rule.source_locator
    assert {(rule.pest_id, rule.symptom_id): rule.source_locator
            for rule in knowledge.rules} == {
        (rule["pest_id"], rule["symptom_id"]): rule["source_locator"]
        for rule in candidate["rules"]
    }

    with pytest.raises(KnowledgeLoadError):
        load_knowledge(VERIFIED_PATH, expected_mode="demo", data_root=DATA_ROOT)


def test_verified_http_flow_has_sources_ranking_and_trace():
    app = verified_app()
    symptoms = call(app, "GET", "/symptoms")
    assert symptoms.status_code == 200
    assert symptoms.json()["mode"] == "verified"
    assert len(symptoms.json()["symptoms"]) == 10
    assert {item["id"] for item in symptoms.json()["symptoms"]} == {
        "G23", "G24", "G25", "G26", "G30", "G31", "G32", "G34", "G36", "G37"
    }

    pest = call(app, "GET", "/pests/P12")
    assert pest.status_code == 200
    assert pest.json()["pest"]["handling"] is None
    assert {source["id"] for source in pest.json()["pest"]["sources"]} == {"SRC-01", "SRC-05"}
    assert all(source["url"].startswith("https://") for source in pest.json()["pest"]["sources"])
    assert call(app, "GET", "/pests/P11").status_code == 404

    payload = {"observations": [
        {"symptom_id": "G30", "cf_user": 1.0},
        {"symptom_id": "G31", "cf_user": 1.0},
        {"symptom_id": "G32", "cf_user": 1.0},
    ]}
    response = call(app, "POST", "/consultations", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["mode"] == "verified" and result["status"] == "supported"
    assert [(item["pest_id"], item["rank"]) for item in result["candidates"]] == [
        ("P12", 1), ("P13", 2)
    ]
    assert result["candidates"][0]["cf"] == pytest.approx(0.952)
    assert [step["symptom_id"] for step in result["trace"] if step["pest_id"] == "P12"] == [
        "G30", "G31", "G32"
    ]
    assert all(step["source_id"] == "SRC-01" and step["source_locator"] for step in result["trace"])
    previous = 0.0
    for step in (item for item in result["trace"] if item["pest_id"] == "P12"):
        assert step["before"] == pytest.approx(previous)
        assert step["after"] == pytest.approx(previous + step["support"] * (1 - previous))
        previous = step["after"]
    assert previous == pytest.approx(result["candidates"][0]["cf"])


def test_shared_symptom_ties_and_empty_input_has_no_support():
    app = verified_app()
    tied = call(app, "POST", "/consultations", json={
        "observations": [{"symptom_id": "G31", "cf_user": 1.0}]
    }).json()
    assert {item["pest_id"] for item in tied["candidates"]} == {"P12", "P13"}
    assert all(item["rank"] == 1 and item["is_tied"] for item in tied["candidates"])
    assert all(item["cf"] == pytest.approx(0.4) for item in tied["candidates"])
    empty = call(app, "POST", "/consultations", json={"observations": []}).json()
    assert empty["mode"] == "verified" and empty["status"] == "no_support"
    assert empty["candidates"] == [] and empty["trace"] == []
