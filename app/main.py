"""FastAPI application and static browser entry point."""

import mimetypes
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from sqlalchemy import Engine, create_engine

from app.api.routes import router
from app.config import AppConfig, read_config
from app.db.store import load_snapshot
from app.services.knowledge_loader import load_knowledge

STATIC_ROOT = (Path(__file__).parent / "static").resolve()


def create_app(config: AppConfig | None = None, *, engine: Engine | None = None) -> FastAPI:
    selected = config if config is not None else read_config()
    if selected.backend == "postgres":
        if selected.mode != "verified" or not selected.knowledge_version:
            raise ValueError("Postgres requires an explicit verified knowledge version")
        if engine is None:
            if not selected.database_url or not selected.database_url.startswith(
                "postgresql+psycopg://"
            ):
                raise ValueError("DATABASE_URL must use postgresql+psycopg")
            engine = create_engine(selected.database_url, pool_pre_ping=True)
        knowledge = load_snapshot(engine, selected.knowledge_version)
    else:
        knowledge = load_knowledge(
            selected.knowledge_path, expected_mode=selected.mode, data_root=selected.data_root
        )
    app = FastAPI(title="Sistem Pakar Identifikasi Hama Tomat", version="0.1.0")
    app.state.knowledge = knowledge
    app.state.db_engine = engine if selected.backend == "postgres" else None
    app.include_router(router)

    @app.get("/", include_in_schema=False)
    async def home() -> Response:
        return Response((STATIC_ROOT / "index.html").read_bytes(), media_type="text/html")

    @app.get("/static/{asset_path:path}", include_in_schema=False)
    async def static_asset(asset_path: str) -> Response:
        path = (STATIC_ROOT / asset_path).resolve()
        if not path.is_relative_to(STATIC_ROOT) or not path.is_file():
            raise HTTPException(status_code=404, detail="not found")
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return Response(path.read_bytes(), media_type=media_type)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(_request: Request, _exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {"code": "invalid_input", "message": "Input konsultasi tidak valid."}
            },
        )

    @app.exception_handler(HTTPException)
    async def http_error(_request: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict) and "error" in exc.detail:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {"code": "http_error", "message": "Permintaan tidak dapat diproses."}
            },
        )

    return app


app = create_app()
