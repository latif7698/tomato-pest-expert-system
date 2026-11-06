"""HTTP input and output contracts for consultations."""

from __future__ import annotations

import math
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.services.cf_engine import USER_CF_VALUES


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ObservationInput(StrictModel):
    symptom_id: str
    cf_user: float

    @field_validator("symptom_id")
    @classmethod
    def nonblank_symptom(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("symptom_id must not be blank")
        return value

    @field_validator("cf_user", mode="before")
    @classmethod
    def valid_user_cf(cls, value: object) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("cf_user must be numeric")
        try:
            number = float(value)
        except OverflowError as exc:
            raise ValueError("cf_user must be finite") from exc
        if not math.isfinite(number) or number not in USER_CF_VALUES:
            raise ValueError("cf_user must use the proposed scale")
        return number


class ConsultationRequest(StrictModel):
    observations: list[ObservationInput]

    @model_validator(mode="after")
    def unique_symptoms(self) -> ConsultationRequest:
        ids = [item.symptom_id for item in self.observations]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate symptom_id")
        return self


class SymptomItem(StrictModel):
    id: str
    label: str


class SymptomsResponse(StrictModel):
    knowledge_version: str
    mode: Literal["demo", "verified"]
    symptoms: list[SymptomItem]


class SourceItem(StrictModel):
    id: str
    title: str
    url: str | None


class PestItem(StrictModel):
    id: str
    name: str
    description: str
    handling: str | None
    sources: list[SourceItem]


class PestResponse(StrictModel):
    knowledge_version: str
    mode: Literal["demo", "verified"]
    pest: PestItem


class CandidateItem(StrictModel):
    pest_id: str
    name: str
    cf: float
    rank: int
    is_tied: bool


class TraceItem(StrictModel):
    pest_id: str
    symptom_id: str
    cf_expert: float
    cf_user: float
    support: float
    before: float
    after: float
    source_id: str
    source_locator: str


class ConsultationResponse(StrictModel):
    knowledge_version: str
    mode: Literal["demo", "verified"]
    status: Literal["supported", "no_support"]
    candidates: list[CandidateItem]
    trace: list[TraceItem]
