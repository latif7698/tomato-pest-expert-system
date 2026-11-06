"""Map validated knowledge and pure CF results to HTTP contracts."""

from dataclasses import asdict

from app.schemas.consultation import (
    CandidateItem,
    ConsultationRequest,
    ConsultationResponse,
    PestItem,
    PestResponse,
    SourceItem,
    SymptomsResponse,
    TraceItem,
)
from app.schemas.knowledge import KnowledgeBase
from app.services.cf_engine import Observation, calculate_cf


def list_symptoms(knowledge: KnowledgeBase) -> SymptomsResponse:
    return SymptomsResponse(
        knowledge_version=knowledge.knowledge_version,
        mode=knowledge.mode,
        symptoms=[{"id": item.id, "label": item.label} for item in knowledge.symptoms],
    )


def get_pest(knowledge: KnowledgeBase, pest_id: str) -> PestResponse | None:
    pest = next((item for item in knowledge.pests if item.id == pest_id), None)
    if pest is None:
        return None
    sources_by_id = {item.id: item for item in knowledge.sources}
    sources = [
        SourceItem(id=source.id, title=source.title, url=source.url)
        for source_id in pest.source_ids
        for source in [sources_by_id[source_id]]
    ]
    return PestResponse(
        knowledge_version=knowledge.knowledge_version,
        mode=knowledge.mode,
        pest=PestItem(
            id=pest.id,
            name=pest.name,
            description=pest.description,
            handling=pest.handling if knowledge.mode == "verified" else None,
            sources=sources,
        ),
    )


def consult(knowledge: KnowledgeBase, request: ConsultationRequest) -> ConsultationResponse:
    observations = [
        Observation(symptom_id=item.symptom_id, cf_user=item.cf_user)
        for item in request.observations
    ]
    result = calculate_cf(knowledge, observations)
    names = {pest.id: pest.name for pest in knowledge.pests}
    return ConsultationResponse(
        knowledge_version=result.knowledge_version,
        mode=result.mode,
        status=result.status,
        candidates=[
            CandidateItem(**asdict(item), name=names[item.pest_id]) for item in result.candidates
        ],
        trace=[TraceItem(**asdict(item)) for item in result.trace],
    )
