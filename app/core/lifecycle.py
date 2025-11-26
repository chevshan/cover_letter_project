from fastapi import FastAPI

from app.core.config import logger
from langgraph_components.cover_letter_worflow import create_workflow
from utils.parsers.pdf_parser import PDFParser


def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup() -> None:
        logger.info("Starting application and preparing resources")
        _ensure_workflow(app)
        _ensure_pdf_parser(app)


def _ensure_workflow(app: FastAPI):
    if getattr(app.state, "workflow", None) is None:
        logger.info("Compiling cover letter workflow")
        app.state.workflow = create_workflow()


def _ensure_pdf_parser(app: FastAPI):
    if getattr(app.state, "pdf_parser", None) is None:
        logger.info("Initializing PDF parser")
        app.state.pdf_parser = PDFParser()
