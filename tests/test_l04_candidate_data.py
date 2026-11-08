"""Integrity checks for the L04 review candidate, outside the application loader."""

import json
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse

import pytest
from pydantic import ValidationError

from app.schemas.knowledge import KnowledgeBase
from app.services.knowledge_loader import KnowledgeLoadError, load_knowledge

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "data" / "review"
CANDIDATE_PATH = REVIEW / "l04_candidate_knowledge.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_is_review_only():
    candidate = read_json(CANDIDATE_PATH)
    assert CANDIDATE_PATH.parent == REVIEW
    assert not CANDIDATE_PATH.is_relative_to(ROOT / "data" / "verified")
    assert set(candidate) == {"_meta", "domain", "pests", "symptoms", "rules", "sources"}
    assert candidate["_meta"] == {
        "status": "candidate_after_human_review",
        "not_for_application_use": True,
        "source_extraction": "l04_extraction.json",
        "source_descriptions": "l04_pest_descriptions_draft.json",
        "reviewer": "Asep Abdul Latip",
        "review_date": "2026-11-08",
        "reviewed_input_sha256": "d43e1924e18dd07f2661f2a669f74015fda09e0c7a984e1a236c9620d3d0d944",
    }
    assert candidate["domain"] == "tomato_pests"
    assert "mode" not in candidate
    assert {rule["validation_status"] for rule in candidate["rules"]} == {"candidate"}
    assert {source["access_status"] for source in candidate["sources"]} == {"reviewed"}
    with pytest.raises(ValidationError):
        KnowledgeBase.model_validate(candidate)
    for mode in ("demo", "verified"):
        application_shape = {key: value for key, value in candidate.items() if key != "_meta"}
        application_shape.update(knowledge_version="l04-review", mode=mode)
        with pytest.raises(ValidationError):
            KnowledgeBase.model_validate(application_shape)
        with pytest.raises(KnowledgeLoadError):
            load_knowledge(CANDIDATE_PATH, expected_mode=mode, data_root=ROOT / "data")


def test_candidate_entities_and_source_references():
    candidate = read_json(CANDIDATE_PATH)
    extraction = read_json(REVIEW / "l04_extraction.json")
    draft = read_json(REVIEW / "l04_pest_descriptions_draft.json")
    register = (ROOT / "docs" / "knowledge" / "SOURCE_REGISTER.md").read_text(encoding="utf-8")
    modeled = [
        row for row in extraction["relations"] if row["mvp_option_b_disposition"] == "dimodelkan"
    ]
    pest_ids = {row["pest_code"] for row in modeled}
    symptom_ids = {row["symptom_code"] for row in modeled}
    source_ids = {source["id"] for source in candidate["sources"]}

    counts = tuple(len(candidate[key]) for key in ("pests", "symptoms", "rules"))
    assert counts == (5, 10, 11)
    assert pest_ids == {"P9", "P10", "P12", "P13", "P14"}
    assert symptom_ids == {"G23", "G24", "G25", "G26", "G30", "G31", "G32", "G34", "G36", "G37"}
    assert source_ids == {"SRC-01", "SRC-02", "SRC-03", "SRC-05", "SRC-06", "SRC-07"}

    pests = {pest["id"]: pest for pest in candidate["pests"]}
    symptoms = {symptom["id"]: symptom for symptom in candidate["symptoms"]}
    assert len(pests) == len(candidate["pests"]) and set(pests) == pest_ids
    assert len(symptoms) == len(candidate["symptoms"]) and set(symptoms) == symptom_ids
    for source in candidate["sources"]:
        assert set(source) == {"id", "title", "url", "access_status"}
        assert source["title"].strip()
        assert source["access_status"] == "reviewed"
        parsed = urlparse(source["url"])
        assert parsed.scheme == "https" and parsed.netloc
        assert f"| {source['id']} |" in register and source["url"] in register

    draft_pests = {pest["id"]: pest for pest in draft["pests"]}
    draft_sources = {source["id"]: source for source in draft["sources"]}
    for source in candidate["sources"]:
        if source["id"] != "SRC-01":
            assert all(source[key] == draft_sources[source["id"]][key] for key in source)
    for pest_id, pest in pests.items():
        assert set(pest) == {"id", "name", "description", "source_ids"}
        assert pest["name"] == draft_pests[pest_id]["name"]
        assert pest["description"] == draft_pests[pest_id]["description"]
        assert pest["description"].strip()
        assert pest["source_ids"] == draft_pests[pest_id]["source_ids"]
        assert set(pest["source_ids"]) <= source_ids
        assert "handling" not in pest

    extracted_symptoms = {symptom["code"]: symptom for symptom in extraction["symptoms"]}
    for symptom_id, symptom in symptoms.items():
        assert set(symptom) == {"id", "label", "source_ids"}
        assert symptom["label"] == extracted_symptoms[symptom_id]["text_printed_table_ii"].rstrip()
        assert symptom["label"] == symptom["label"].rstrip()
        assert symptom["source_ids"] == ["SRC-01"]


def test_rules_match_transcription_and_omissions_remain_in_extraction():
    candidate = read_json(CANDIDATE_PATH)
    extraction = read_json(REVIEW / "l04_extraction.json")
    relations = extraction["relations"]
    modeled = {
        (row["pest_code"], row["symptom_code"]): row
        for row in relations
        if row["mvp_option_b_disposition"] == "dimodelkan"
    }
    omitted = [row for row in relations if row["mvp_option_b_disposition"] != "dimodelkan"]
    assert len(relations) == 19 and len(modeled) == 11 and len(omitted) == 8
    negative = [
        row for row in omitted if row["mvp_option_b_disposition"] == "tidak_dimodelkan_cf_negatif"
    ]
    held = [
        row for row in omitted if row["mvp_option_b_disposition"] == "ditahan_di_review_p11_d19"
    ]
    assert len(negative) == 6 and len(held) == 2
    assert all(row["pest_code"] == "P11" for row in held)
    for row in relations:
        calculated = Decimal(str(row["mb_transcribed"])) - Decimal(str(row["md_transcribed"]))
        assert calculated == Decimal(str(row["cf_expert_calc_mb_minus_md"]))
        if row in negative:
            assert calculated < 0

    pairs = [(rule["pest_id"], rule["symptom_id"]) for rule in candidate["rules"]]
    assert len(pairs) == len(set(pairs)) and set(pairs) == set(modeled)
    assert not set(pairs) & {(row["pest_code"], row["symptom_code"]) for row in omitted}
    assert all(rule["pest_id"] != "P11" for rule in candidate["rules"])
    assert not {rule["symptom_id"] for rule in candidate["rules"]} & {
        "G7", "G12", "G17", "G27", "G28", "G29", "G33", "G35"
    }

    for rule in candidate["rules"]:
        assert set(rule) == {
            "pest_id", "symptom_id", "cf_expert", "source_id", "source_locator",
            "validation_status",
        }
        row = modeled[(rule["pest_id"], rule["symptom_id"])]
        calculated = Decimal(str(row["mb_transcribed"])) - Decimal(str(row["md_transcribed"]))
        assert calculated == Decimal(str(row["cf_expert_calc_mb_minus_md"]))
        assert Decimal(str(rule["cf_expert"])) == calculated
        assert 0 < calculated <= 1
        assert rule["source_id"] == "SRC-01"
        source = row["source"]
        assert rule["source_locator"] == (
            f"hal. cetak {source['printed_page']}, {source['table']}, {source['locator']}"
        )
        assert "Tabel IV" in rule["source_locator"] and rule["source_locator"].strip()
        assert rule["validation_status"] == "candidate"

    shared = [rule for rule in candidate["rules"] if rule["symptom_id"] == "G31"]
    assert {rule["pest_id"] for rule in shared} == {"P12", "P13"}
    assert len({rule["cf_expert"] for rule in shared}) == 1
