import json
from typing import Dict, Any

from custom_llm import CustomLLM


class CriticAgent:
    def __init__(self, llm: CustomLLM, min_score: float = 0.7, max_revisions: int = 3):
        self.llm = llm
        self.min_score = min_score
        self.max_revisions = max_revisions

    def review_cover_letter(self, state: Dict[str, Any]) -> Dict[str, Any]:
        draft = state.get("draft_cover_letter", "").strip()
        if not draft:
            return {
                "cover_letter_feedback": "No cover letter draft available for review.",
                "cover_letter_score": 0.0,
                "needs_revision": False,
            }

        vacancy_analysis = state.get("vacancy_analysis", "")
        resume_analysis = state.get("resume_analysis", "")
        analysis_report = state.get("analysis_report", "")
        revision_attempts = state.get("revision_attempts", 0)

        system_prompt = (
            "You are a meticulous HR editor. Critically evaluate cover letters "
            "against job requirements and provide actionable revision guidance."
        )
        prompt = f"""
        Review the following cover letter draft. Score it from 0 to 1, where 1 means the
        letter is ready to send without changes. Highlight concrete issues that must be fixed.

        Return ONLY valid minified JSON with fields:
        - "score": number between 0 and 1
        - "feedback": short paragraph with improvement tips
        - "issues": bullet-style array with specific issues referencing parts of the letter

        COVER LETTER DRAFT:
        {draft}

        JOB ANALYSIS:
        {vacancy_analysis}

        CANDIDATE ANALYSIS:
        {resume_analysis}

        MATCH REPORT:
        {analysis_report}
        """

        raw_response = self.llm.invoke(prompt, system_prompt)
        parsed_response = self._parse_response(raw_response)

        score = parsed_response.get("score", 0.0)
        feedback_sections = []

        if parsed_response.get("feedback"):
            feedback_sections.append(parsed_response["feedback"].strip())

        issues = parsed_response.get("issues", [])
        if isinstance(issues, list) and issues:
            bullet_list = "\n".join(f"- {issue}" for issue in issues if isinstance(issue, str))
            if bullet_list:
                feedback_sections.append(f"Key issues:\n{bullet_list}")

        needs_revision = score < self.min_score and revision_attempts < self.max_revisions
        if score < self.min_score and revision_attempts >= self.max_revisions:
            feedback_sections.append(
                f"Revision limit reached ({self.max_revisions}). "
                "Use the latest draft as the final version."
            )

        feedback = "\n\n".join(feedback_sections).strip()

        result: Dict[str, Any] = {
            "cover_letter_feedback": feedback,
            "cover_letter_score": score,
            "needs_revision": needs_revision,
        }

        if not needs_revision:
            result["cover_letter"] = draft

        return result

    def _parse_response(self, raw_response: str) -> Dict[str, Any]:
        if not raw_response:
            return {}

        raw_response = raw_response.strip()

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            # Attempt to extract JSON substring if the model wrapped it in text.
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(raw_response[start : end + 1])
                except json.JSONDecodeError:
                    pass
        return {}

