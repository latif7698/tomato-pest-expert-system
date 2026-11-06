"""Independent numerical tests for the pure CF engine."""

import pytest

from app.schemas.knowledge import KnowledgeBase
from app.services.cf_engine import Observation, calculate_cf


def test_single_symptom(sample_knowledge):
    result = calculate_cf(sample_knowledge, [Observation("G_SYN_1", 1.0)])
    assert result.status == "supported"
    assert result.candidates[0].cf == pytest.approx(0.8)
    assert result.trace[0].before == 0
    assert result.trace[0].after == pytest.approx(0.8)
    assert result.mode == "demo"
    assert result.knowledge_version == "demo-001"


def test_two_supports_make_point_eight_six_and_trace_reconstructs(sample_knowledge):
    result = calculate_cf(
        sample_knowledge, [Observation("G_SYN_1", 1), Observation("G_SYN_2", 0.5)]
    )
    assert result.candidates[0].cf == pytest.approx(0.86)
    assert [step.support for step in result.trace] == pytest.approx([0.8, 0.3])
    previous = 0.0
    for step in result.trace:
        assert step.before == pytest.approx(previous)
        assert step.after == pytest.approx(previous + step.support * (1 - previous))
        assert step.source_id == "S_SYN"
        assert step.source_locator == "fixture sintetis"
        previous = step.after
    assert previous == pytest.approx(result.candidates[0].cf)


def test_empty_and_zero_support_have_no_candidates(sample_knowledge, sample_payload):
    empty = calculate_cf(sample_knowledge, [])
    assert (empty.status, empty.candidates, empty.trace) == ("no_support", (), ())
    sample_payload["rules"][0]["cf_expert"] = 0
    sample_payload["rules"][1]["cf_expert"] = 0
    zero_knowledge = KnowledgeBase.model_validate(sample_payload)
    zero = calculate_cf(zero_knowledge, [Observation("G_SYN_1", 1)])
    assert (zero.status, zero.candidates, zero.trace) == ("no_support", (), ())


def test_tie_and_ordering(sample_payload):
    second = dict(sample_payload["pests"][0])
    second["id"] = "P_SYN_0"
    sample_payload["pests"].append(second)
    extra = dict(sample_payload["rules"][0])
    extra["pest_id"] = "P_SYN_0"
    sample_payload["rules"].append(extra)
    knowledge = KnowledgeBase.model_validate(sample_payload)
    result = calculate_cf(knowledge, [Observation("G_SYN_1", 1)])
    assert [candidate.pest_id for candidate in result.candidates] == ["P_SYN_0", "P_SYN_1"]
    assert [candidate.rank for candidate in result.candidates] == [1, 1]
    assert all(candidate.is_tied for candidate in result.candidates)


def test_candidates_have_independent_scores_and_competition_ranks(sample_payload):
    second = dict(sample_payload["pests"][0])
    second["id"] = "P_SYN_2"
    sample_payload["pests"].append(second)
    extra = dict(sample_payload["rules"][0])
    extra["pest_id"] = "P_SYN_2"
    extra["cf_expert"] = 0.4
    sample_payload["rules"].append(extra)
    result = calculate_cf(
        KnowledgeBase.model_validate(sample_payload),
        [Observation("G_SYN_1", 1), Observation("G_SYN_2", 0.5)],
    )
    assert [(item.pest_id, item.rank, item.is_tied) for item in result.candidates] == [
        ("P_SYN_1", 1, False),
        ("P_SYN_2", 2, False),
    ]
    assert [item.cf for item in result.candidates] == pytest.approx([0.86, 0.4])
    assert result.trace[-1].pest_id == "P_SYN_2"


def test_near_equal_scores_are_marked_as_tied(sample_payload):
    second = dict(sample_payload["pests"][0])
    second["id"] = "P_SYN_0"
    sample_payload["pests"].append(second)
    extra = dict(sample_payload["rules"][0])
    extra["pest_id"] = "P_SYN_0"
    extra["cf_expert"] = 0.8 - 5e-13
    sample_payload["rules"].append(extra)
    result = calculate_cf(KnowledgeBase.model_validate(sample_payload), [Observation("G_SYN_1", 1)])
    assert [item.pest_id for item in result.candidates] == ["P_SYN_0", "P_SYN_1"]
    assert [item.rank for item in result.candidates] == [1, 1]
    assert all(item.is_tied for item in result.candidates)


def test_input_order_does_not_change_result(sample_knowledge):
    first = calculate_cf(sample_knowledge, [Observation("G_SYN_1", 1), Observation("G_SYN_2", 0.5)])
    second = calculate_cf(sample_knowledge, [Observation("G_SYN_2", 0.5), Observation("G_SYN_1", 1)])
    assert abs(first.candidates[0].cf - second.candidates[0].cf) <= 1e-12
    assert first.trace == second.trace


@pytest.mark.parametrize(
    "observations",
    [
        [Observation("missing", 1)],
        [Observation("G_SYN_1", 1), Observation("G_SYN_1", 0.5)],
        [Observation("G_SYN_1", 0)],
        [Observation("G_SYN_1", 1.1)],
        [Observation("G_SYN_1", float("nan"))],
        [Observation("G_SYN_1", float("inf"))],
        [Observation("G_SYN_1", True)],
        [Observation("G_SYN_1", "1.0")],
        [Observation("G_SYN_1", 10**400)],
    ],
)
def test_rejects_invalid_observation(sample_knowledge, observations):
    with pytest.raises(ValueError):
        calculate_cf(sample_knowledge, observations)
