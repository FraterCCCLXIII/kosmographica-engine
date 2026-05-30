"""FastAPI application factory (REST/JSON, ADR-014)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import audit, entities, reconcile, search


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kosmographica Engine API",
        version="0.1.0",
        summary="Read + audit surface over the canonical claim graph.",
    )
    # The read-only Audit Console (web/) is a separate origin in dev (port varies).
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"http://localhost:\d+",
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["meta"])
    def healthz():
        return {"status": "ok"}

    app.include_router(entities.router)
    app.include_router(search.router)
    app.include_router(audit.router)
    app.include_router(reconcile.router)
    return app


app = create_app()
