from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, HttpUrl, model_validator


class CoverLetterRequest(BaseModel):
    vacancy_url: Optional[HttpUrl] = Field(None, description="Link to the vacancy on hh.ru")
    vacancy_text: Optional[str] = Field(None, description="Raw vacancy description")
    resume_pdf_path: Optional[str] = Field(None, description="Path to resume PDF on disk")
    resume_text: Optional[str] = Field(None, description="Resume plain text")
    save_cover_letter: bool = Field(False, description="Persist generated cover letter to disk")
    output_file: Optional[str] = Field(None, description="Path to store cover letter when save_cover_letter is true")

    @model_validator(mode="after")
    def validate_sources(cls, model):
        if not model.vacancy_url and not model.vacancy_text:
            raise ValueError("Either vacancy_url or vacancy_text must be provided")

        if not model.resume_pdf_path and not model.resume_text:
            raise ValueError("Either resume_pdf_path or resume_text must be provided")

        return model


class CoverLetterResponse(BaseModel):
    cover_letter: str
    vacancy_id: Optional[str] = None
    saved_to: Optional[str] = None
    workflow_report: Dict[str, Any]