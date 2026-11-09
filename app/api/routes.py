"""Thin API endpoints with controlled error responses."""

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.store import save_consultation
from app.schemas.consultation import (
    ConsultationRequest,
    ConsultationResponse,
    PestResponse,
    SymptomsResponse,
)
from app.services.consultation_service import consult, get_pest, list_symptoms

router = APIRouter()


@router.get("/healthz")
def health(request: Request) -> dict[str, str]:
    engine = request.app.state.db_engine
    if engine is not None:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "code": "storage_unavailable",
                        "message": "Penyimpanan sedang tidak tersedia.",
                    }
                },
            ) from exc
    return {"status": "ok"}


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
def create_consultation(payload: ConsultationRequest, request: Request) -> ConsultationResponse:
    try:
        result = consult(request.app.state.knowledge, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": {"code": "invalid_input", "message": "Input konsultasi tidak valid."}},
        ) from exc
    engine = request.app.state.db_engine
    if engine is not None and request.app.state.persist_consultations:
        try:
            save_consultation(engine, payload, result)
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": {
                        "code": "storage_unavailable",
                        "message": "Penyimpanan sedang tidak tersedia.",
                    }
                },
            ) from exc
    return result
