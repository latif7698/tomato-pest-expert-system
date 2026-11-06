"""Schema and integrity checks for one knowledge snapshot."""

from __future__ import annotations

import math
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class Source(StrictModel):
    id: str
    title: str
    url: str | None
    access_status: Literal["synthetic", "reviewed"]

    @field_validator("url")
    @classmethod
    def safe_web_url(cls, value: str | None) -> str | None:
        if value is not None:
            parsed = urlparse(value)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError("source URL must be HTTP or HTTPS")
        return value


class Pest(StrictModel):
    id: str
    name: str
    description: str
    source_ids: list[str]
    handling: str | None = None


class Symptom(StrictModel):
    id: str
    label: str
    source_ids: list[str]


class Rule(StrictModel):
    pest_id: str
    symptom_id: str
    cf_expert: float
    source_id: str
    source_locator: str
    validation_status: Literal["synthetic", "verified"]

    @field_validator("cf_expert", mode="before")
    @classmethod
    def check_cf_expert(cls, value: object) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("cf_expert must be numeric, not boolean")
        try:
            number = float(value)
        except OverflowError as exc:
            raise ValueError("cf_expert must be finite and between 0 and 1") from exc
        if not math.isfinite(number) or not 0 <= number <= 1:
            raise ValueError("cf_expert must be finite and between 0 and 1")
        return number


class KnowledgeBase(StrictModel):
    knowledge_version: str
    domain: Literal["tomato_pests"]
    mode: Literal["demo", "verified"]
    pests: list[Pest]
    symptoms: list[Symptom]
    rules: list[Rule]
    sources: list[Source]

    @model_validator(mode="after")
    def check_integrity(self) -> KnowledgeBase:
        if not self.knowledge_version.strip():
            raise ValueError("knowledge_version must not be blank")

        collections = (self.pests, self.symptoms, self.sources)
        for items in collections:
            ids = [item.id for item in items]
            if any(not item_id.strip() for item_id in ids) or len(ids) != len(set(ids)):
                raise ValueError("entity IDs must be nonblank and unique")

        pest_ids = {pest.id for pest in self.pests}
        symptom_ids = {symptom.id for symptom in self.symptoms}
        source_ids = {source.id for source in self.sources}
        for pest in self.pests:
            if not pest.name.strip() or not pest.description.strip():
                raise ValueError("pest name and description must not be blank")
            if not pest.source_ids or len(pest.source_ids) != len(set(pest.source_ids)):
                raise ValueError("pest source_ids must be nonempty and unique")
            if not set(pest.source_ids) <= source_ids:
                raise ValueError("pest references unknown source")
            if pest.handling is not None and self.mode != "verified":
                raise ValueError("handling requires verified knowledge")
        for symptom in self.symptoms:
            if not symptom.label.strip():
                raise ValueError("symptom label must not be blank")
            if not symptom.source_ids or len(symptom.source_ids) != len(set(symptom.source_ids)):
                raise ValueError("symptom source_ids must be nonempty and unique")
            if not set(symptom.source_ids) <= source_ids:
                raise ValueError("symptom references unknown source")

        for source in self.sources:
            if not source.title.strip():
                raise ValueError("source title must not be blank")
            if self.mode == "demo" and source.access_status != "synthetic":
                raise ValueError("demo source must be synthetic")
            if self.mode == "verified" and (
                source.access_status != "reviewed" or not source.url
            ):
                raise ValueError("verified source requires reviewed status and URL")

        pairs: set[tuple[str, str]] = set()
        expected_status = "synthetic" if self.mode == "demo" else "verified"
        for rule in self.rules:
            pair = (rule.pest_id, rule.symptom_id)
            if pair in pairs:
                raise ValueError("duplicate pest/symptom rule")
            pairs.add(pair)
            if rule.pest_id not in pest_ids or rule.symptom_id not in symptom_ids:
                raise ValueError("rule references unknown pest or symptom")
            if rule.source_id not in source_ids:
                raise ValueError("rule references unknown source")
            if not rule.source_locator.strip():
                raise ValueError("rule source_locator must not be blank")
            if rule.validation_status != expected_status:
                raise ValueError("rule validation_status does not match mode")
        return self
