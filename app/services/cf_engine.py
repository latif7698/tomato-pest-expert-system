"""Pure positive-support Certainty Factor calculation."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from app.schemas.knowledge import KnowledgeBase

USER_CF_VALUES = frozenset((0.25, 0.5, 0.75, 1.0))
TIE_TOLERANCE = 1e-12


@dataclass(frozen=True)
class Observation:
    symptom_id: str
    cf_user: float


@dataclass(frozen=True)
class TraceStep:
    pest_id: str
    symptom_id: str
    cf_expert: float
    cf_user: float
    support: float
    before: float
    after: float
    source_id: str
    source_locator: str


@dataclass(frozen=True)
class Candidate:
    pest_id: str
    cf: float
    rank: int
    is_tied: bool


@dataclass(frozen=True)
class CFResult:
    knowledge_version: str
    mode: Literal["demo", "verified"]
    status: Literal["supported", "no_support"]
    candidates: tuple[Candidate, ...]
    trace: tuple[TraceStep, ...]


def calculate_cf(knowledge: KnowledgeBase, observations: Sequence[Observation]) -> CFResult:
    """Calculate each candidate independently from validated knowledge.

    Observation validation is kept here until the consultation schema is added.
    """
    known_symptoms = {symptom.id for symptom in knowledge.symptoms}
    selected: dict[str, float] = {}
    for observation in observations:
        if not isinstance(observation, Observation):
            # Keep all invalid observations under the same ValueError contract.
            raise ValueError("observation has invalid structure")  # noqa: TRY004
        if observation.symptom_id not in known_symptoms:
            raise ValueError("unknown symptom_id")
        value = observation.cf_user
        try:
            finite = math.isfinite(value) if isinstance(value, (int, float)) else False
        except OverflowError:
            finite = False
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not finite
            or value not in USER_CF_VALUES
        ):
            raise ValueError("cf_user must be one of the proposed scale values")
        if observation.symptom_id in selected:
            raise ValueError("duplicate symptom_id")
        selected[observation.symptom_id] = float(value)

    scores: dict[str, float] = {}
    trace: list[TraceStep] = []
    for rule in sorted(knowledge.rules, key=lambda item: (item.pest_id, item.symptom_id)):
        if rule.symptom_id not in selected:
            continue
        support = rule.cf_expert * selected[rule.symptom_id]
        if support <= 0:
            continue
        before = scores.get(rule.pest_id, 0.0)
        after = before + support * (1 - before)
        scores[rule.pest_id] = after
        trace.append(
            TraceStep(
                pest_id=rule.pest_id,
                symptom_id=rule.symptom_id,
                cf_expert=rule.cf_expert,
                cf_user=selected[rule.symptom_id],
                support=support,
                before=before,
                after=after,
                source_id=rule.source_id,
                source_locator=rule.source_locator,
            )
        )

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    groups: list[list[tuple[str, float]]] = []
    for item in ordered:
        if groups and abs(groups[-1][0][1] - item[1]) <= TIE_TOLERANCE:
            groups[-1].append(item)
        else:
            groups.append([item])
    candidates: list[Candidate] = []
    for group in groups:
        rank = len(candidates) + 1
        for pest_id, score in sorted(group, key=lambda item: item[0]):
            candidates.append(
                Candidate(pest_id=pest_id, cf=score, rank=rank, is_tied=len(group) > 1)
            )

    return CFResult(
        knowledge_version=knowledge.knowledge_version,
        mode=knowledge.mode,
        status="supported" if candidates else "no_support",
        candidates=tuple(candidates),
        trace=tuple(trace),
    )
