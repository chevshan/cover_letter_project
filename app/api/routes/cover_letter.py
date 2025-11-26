from fastapi import APIRouter, HTTPException, Request

from app.schemas.cover_letter import CoverLetterRequest, CoverLetterResponse
from app.services.cover_letter_service import (
    get_or_create_pdf_parser,
    get_or_create_workflow,
    resolve_resume_payload,
    resolve_vacancy_payload,
    run_workflow,
    save_cover_letter,
)


router = APIRouter()


@router.post(
    "/generate-cover-letter",
    response_model=CoverLetterResponse,
    summary="Generate a tailored cover letter",
)
async def generate_cover_letter_endpoint(payload: CoverLetterRequest, request: Request):
    app_state = request.app.state

    vacancy_text, vacancy_id = resolve_vacancy_payload(payload)
    pdf_parser = get_or_create_pdf_parser(app_state)
    resume_text = resolve_resume_payload(payload, pdf_parser)
    workflow = get_or_create_workflow(app_state)

    report = run_workflow(vacancy_text, resume_text, workflow)
    cover_letter = report.get("cover_letter") if isinstance(report, dict) else None
    if not cover_letter:
        raise HTTPException(
            status_code=500,
            detail="Workflow did not return a cover letter",
        )

    saved_to = None
    if payload.save_cover_letter:
        output_path = payload.output_file or "cover_letter.txt"
        saved_to = save_cover_letter(cover_letter, output_path)

    return CoverLetterResponse(
        cover_letter=cover_letter,
        vacancy_id=vacancy_id,
        saved_to=saved_to,
        workflow_report=report,
    )
