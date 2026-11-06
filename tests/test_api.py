"""HTTP contracts for the synthetic demo application."""

import asyncio
import json

import httpx
import pytest

from app.config import AppConfig, read_config
from app.main import create_app
from app.services.knowledge_loader import KnowledgeLoadError


def call(app, method: str, path: str, **kwargs) -> httpx.Response:
    async def perform() -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(perform())


def app_with_payload(tmp_path, sample_payload):
    demo_dir = tmp_path / "demo"
    demo_dir.mkdir(parents=True)
    path = demo_dir / "knowledge_demo.json"
    path.write_text(json.dumps(sample_payload), encoding="utf-8")
    return create_app(AppConfig(mode="demo", data_root=tmp_path, knowledge_path=path))


def test_home_and_static_assets_have_demo_disclaimer():
    app = create_app()
    home = call(app, "GET", "/")
    assert home.status_code == 200
    assert "bukan identifikasi pasti" in home.text
    assert "Data dalam mode demo sepenuhnya sintetis" in home.text
    script = call(app, "GET", "/static/js/consultation.js")
    assert script.status_code == 200
    assert script.headers["content-type"].startswith("text/javascript")
    assert "getSymptoms" in script.text
    assert call(app, "GET", "/static/css/styles.css").headers["content-type"].startswith(
        "text/css"
    )
    assert call(app, "GET", "/static/missing.js").status_code == 404


def test_symptoms_and_pest_detail_from_active_demo():
    app = create_app()
    symptoms = call(app, "GET", "/symptoms")
    assert symptoms.status_code == 200
    assert symptoms.json() == {
        "knowledge_version": "demo-001",
        "mode": "demo",
        "symptoms": [
            {"id": "G_SYN_1", "label": "Gejala sintetis A"},
            {"id": "G_SYN_2", "label": "Gejala sintetis B"},
        ],
    }
    pest = call(app, "GET", "/pests/P_SYN_1")
    assert pest.status_code == 200
    body = pest.json()
    assert body["mode"] == "demo"
    assert body["knowledge_version"] == "demo-001"
    assert body["pest"]["handling"] is None
    assert body["pest"]["sources"] == [
        {"id": "S_SYN", "title": "Fixture sintetis, bukan referensi domain", "url": None}
    ]
    missing = call(app, "GET", "/pests/not-found")
    assert missing.status_code == 404
    assert missing.json() == {
        "error": {"code": "pest_not_found", "message": "Hama tidak ditemukan."}
    }


def test_consultation_has_ranking_and_reconstructable_trace():
    app = create_app()
    payload = {
        "observations": [
            {"symptom_id": "G_SYN_1", "cf_user": 1.0},
            {"symptom_id": "G_SYN_2", "cf_user": 0.5},
        ]
    }
    response = call(app, "POST", "/consultations", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "demo"
    assert body["knowledge_version"] == "demo-001"
    assert body["status"] == "supported"
    assert body["candidates"] == [
        {
            "pest_id": "P_SYN_1",
            "name": "Hama sintetis A",
            "cf": pytest.approx(0.86),
            "rank": 1,
            "is_tied": False,
        }
    ]
    assert [item["support"] for item in body["trace"]] == pytest.approx([0.8, 0.3])
    assert body["trace"][-1]["after"] == pytest.approx(body["candidates"][0]["cf"])
    assert all(item["source_id"] == "S_SYN" for item in body["trace"])
    assert call(app, "POST", "/consultations", json=payload).json() == body
    assert not hasattr(app.state, "consultation_history")


def test_empty_and_valid_unmatched_observations_have_no_support(tmp_path, sample_payload):
    app = app_with_payload(tmp_path, sample_payload)
    empty = call(app, "POST", "/consultations", json={"observations": []})
    assert empty.status_code == 200
    assert empty.json() == {
        "knowledge_version": "demo-001",
        "mode": "demo",
        "status": "no_support",
        "candidates": [],
        "trace": [],
    }
    sample_payload["symptoms"].append(
        {"id": "G_SYN_3", "label": "Gejala sintetis tanpa aturan", "source_ids": ["S_SYN"]}
    )
    other_app = app_with_payload(tmp_path / "other", sample_payload)
    unmatched = call(
        other_app,
        "POST",
        "/consultations",
        json={"observations": [{"symptom_id": "G_SYN_3", "cf_user": 1.0}]},
    )
    assert unmatched.status_code == 200
    assert unmatched.json()["status"] == "no_support"
    assert unmatched.json()["candidates"] == []


@pytest.mark.parametrize("confidence", [0.25, 0.5, 0.75, 1.0])
def test_each_proposed_user_confidence_is_accepted(confidence):
    response = call(
        create_app(),
        "POST",
        "/consultations",
        json={"observations": [{"symptom_id": "G_SYN_1", "cf_user": confidence}]},
    )
    assert response.status_code == 200
    assert response.json()["candidates"][0]["cf"] == pytest.approx(0.8 * confidence)


@pytest.mark.parametrize(
    "content",
    [
        '{}',
        '{"observations":"wrong"}',
        '{broken',
        '{"observations":[{"symptom_id":"G_SYN_1"}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":1.0},'
        '{"symptom_id":"G_SYN_1","cf_user":0.5}]}',
        '{"observations":[{"symptom_id":"missing","cf_user":1.0}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":0}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":1.1}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":NaN}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":"1.0"}]}',
        '{"observations":[{"symptom_id":"G_SYN_1","cf_user":true}]}',
    ],
)
def test_invalid_requests_are_422_without_internal_details(content):
    response = call(
        create_app(),
        "POST",
        "/consultations",
        content=content,
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "error": {"code": "invalid_input", "message": "Input konsultasi tidak valid."}
    }
    assert "Traceback" not in response.text
    assert "/mnt/" not in response.text


def test_tied_candidates_share_rank(tmp_path, sample_payload):
    another = dict(sample_payload["pests"][0])
    another["id"] = "P_SYN_0"
    sample_payload["pests"].append(another)
    rule = dict(sample_payload["rules"][0])
    rule["pest_id"] = "P_SYN_0"
    sample_payload["rules"].append(rule)
    app = app_with_payload(tmp_path, sample_payload)
    result = call(
        app,
        "POST",
        "/consultations",
        json={"observations": [{"symptom_id": "G_SYN_1", "cf_user": 1.0}]},
    ).json()
    assert [item["pest_id"] for item in result["candidates"]] == ["P_SYN_0", "P_SYN_1"]
    assert [item["rank"] for item in result["candidates"]] == [1, 1]
    assert all(item["is_tied"] for item in result["candidates"])


def test_verified_mode_missing_data_fails_without_demo_fallback(tmp_path):
    config = AppConfig(
        mode="verified",
        data_root=tmp_path,
        knowledge_path=tmp_path / "verified" / "knowledge_verified.json",
    )
    with pytest.raises(KnowledgeLoadError):
        create_app(config)


def test_verified_environment_never_selects_demo(monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_MODE", "verified")
    selected = read_config()
    assert selected.mode == "verified"
    assert selected.knowledge_path.name == "knowledge_verified.json"
    with pytest.raises(KnowledgeLoadError):
        create_app(selected)
