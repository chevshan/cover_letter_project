from typing import TypedDict

class CoverLetterState(TypedDict):
    vacancy_description: str
    resume: str
    vacancy_analysis: str
    resume_analysis: str
    analysis_report: str
    draft_cover_letter: str
    cover_letter: str
    cover_letter_feedback: str
    cover_letter_score: float
    needs_revision: bool
    revision_attempts: int