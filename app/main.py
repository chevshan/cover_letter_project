from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.lifecycle import register_startup_event


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cover Letter Generator",
        description="Generate cover letters by analyzing a vacancy and a resume."
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_startup_event(app)
    app.include_router(api_router)
    return app

app = create_app()