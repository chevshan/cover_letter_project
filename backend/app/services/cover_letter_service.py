import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from fastapi import HTTPException

from app.core.config import logger
from langgraph_components.cover_letter_worflow import create_workflow
from langgraph_components.generate_cover_letter import generate_cover_letter
from utils.parsers.extract_vacancy_id import extract_vacancy_id
from utils.parsers.pdf_parser import PDFParser
from utils.parsers.vacancy_description_parser import extract_vacancy_description
from app.schemas.cover_letter import CoverLetterRequest

UPLOADS_DIR = Path("/app/uploads")

def resolve_vacancy_payload(request_data: CoverLetterRequest) -> Tuple[str, Optional[str]]:
    vacancy_text = request_data.vacancy_text
    vacancy_id: Optional[str] = None

    if request_data.vacancy_url:
        try:
            vacancy_id = extract_vacancy_id(str(request_data.vacancy_url))
            logger.info("Resolved vacancy id %s from url", vacancy_id)
        except ValueError as exc:
            logger.warning("Failed to extract vacancy id: %s", exc)
            vacancy_id = None

    if not vacancy_text:
        if not request_data.vacancy_url or not vacancy_id:
            raise HTTPException(
                status_code=422,
                detail="Valid vacancy_url or vacancy_text must be provided",
            )
        try:
            vacancy_text = extract_vacancy_description(vacancy_id)
            logger.info("Fetched vacancy description for id %s", vacancy_id)
        except Exception as exc:
            logger.exception("Failed to fetch vacancy description")
            raise HTTPException(
                status_code=502,
                detail=f"Unable to fetch vacancy description: {exc}",
            ) from exc

    return vacancy_text, vacancy_id


def resolve_resume_payload(
    request_data: CoverLetterRequest, pdf_parser: Optional[PDFParser]
) -> str:
    if request_data.resume_text:
        return request_data.resume_text

    if not request_data.resume_pdf_path:
        raise HTTPException(
            status_code=422,
            detail="resume_pdf_path must be provided when resume_text is missing",
        )

    filename = request_data.resume_pdf_path
    if "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = UPLOADS_DIR / filename

    try:
        file_path = file_path.resolve(strict=False)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not str(file_path).startswith(str(UPLOADS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Access denied")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Resume file not found: {filename}")

    if pdf_parser is None:
        logger.error("PDF parser is not initialized")
        raise HTTPException(status_code=500, detail="PDF parser is not initialized")

    try:
        resume_text = pdf_parser.parse_pdf(str(file_path))
        logger.info("Parsed resume from %s", file_path)
        return resume_text
    except Exception as exc:
        logger.exception("Failed to parse resume PDF")
        raise HTTPException(
            status_code=502,
            detail=f"Unable to parse resume PDF: {exc}",
        ) from exc


def get_or_create_workflow(app_state) -> Any:
    workflow = getattr(app_state, "workflow", None)
    if workflow is None:
        workflow = create_workflow()
        app_state.workflow = workflow
    return workflow


def get_or_create_pdf_parser(app_state) -> PDFParser:
    pdf_parser = getattr(app_state, "pdf_parser", None)
    if pdf_parser is None:
        pdf_parser = PDFParser()
        app_state.pdf_parser = pdf_parser
    return pdf_parser


def run_workflow(vacancy_text: str, resume_text: str, workflow) -> Dict[str, Any]:
    try:
        logger.info("Starting workflow execution")
        report = generate_cover_letter(vacancy_text, resume_text, workflow)
        logger.info("Workflow execution finished successfully")
        return report
    except Exception as exc:
        logger.exception("Workflow execution failed")
        raise HTTPException(status_code=500, detail=f"Workflow failed: {exc}") from exc


def save_cover_letter(cover_letter: str, output_file: Optional[str]) -> Optional[str]:
    if output_file is None:
        return None
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cover_letter)
        saved_to = os.path.abspath(output_file)
        logger.info("Cover letter saved to %s", saved_to)
        return saved_to
    except OSError as exc:
        logger.exception("Failed to save cover letter")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to save cover letter: {exc}",
        ) from exc
