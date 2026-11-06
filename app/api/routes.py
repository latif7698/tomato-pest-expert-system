"""Thin API endpoints with controlled error responses."""

from fastapi import APIRouter, HTTPException, Request

from app.schemas.consultation import (
    ConsultationRequest,
    ConsultationResponse,
    PestResponse,
    SymptomsResponse,
)
from app.services.consultation_service import consult, get_pest, list_symptoms

router = APIRouter()


@router.get("/symptoms", response_model=SymptomsResponse)
async def symptoms(request: Request) -> SymptomsResponse:
    return list_symptoms(request.app.state.knowledge)


@router.get("/pests/{pest_id}", response_model=PestResponse)
async def pest_detail(pest_id: str, request: Request) -> PestResponse:
    result = get_pest(request.app.state.knowledge, pest_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "pest_not_found", "message": "Hama tidak ditemukan."}},
        )
    return result


@router.post("/consultations", response_model=ConsultationResponse)
async def create_consultation(
    payload: ConsultationRequest, request: Request
) -> ConsultationResponse:
    try:
        return consult(request.app.state.knowledge, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": {"code": "invalid_input", "message": "Input konsultasi tidak valid."}},
        ) from exc
