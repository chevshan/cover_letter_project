from typing import Dict, Any
from custom_llm import CustomLLM

class CopyWriterAgent:
    def __init__(self, llm: CustomLLM):
        self.llm = llm
    
    def generate_cover_letter(self, state: Dict[str, Any]) -> Dict[str, Any]:
        analysis_report = state.get("analysis_report", "")
        vacancy_analysis = state.get("vacancy_analysis", "")
        resume_analysis = state.get("resume_analysis", "")
        reviewer_feedback = state.get("cover_letter_feedback", "").strip()
        revision_attempts = state.get("revision_attempts", 0)

        system_prompt = """You are a professional HR specialist with expertise in writing cover letters. 
        Create concise, professional cover letters that are ready to send immediately.
        
        CRITICAL: Return ONLY the cover letter text without:
        - Headers like "Cover Letter"
        - Analysis or reports
        - Markdown formatting
        - Comments or explanations
        - Generic closings like "Sincerely yours"
        
        The letter must be ready to copy and send to employers."""

        feedback_section = ""
        if reviewer_feedback:
            feedback_section = f"""
        REVIEWER FEEDBACK (MUST ADDRESS EACH POINT):
        {reviewer_feedback}
        """

        prompt = f"""
        Based on the job and candidate analysis, create a cover letter.

        JOB REQUIREMENTS:
        {vacancy_analysis}

        CANDIDATE QUALIFICATIONS:
        {resume_analysis}

        KEY MATCHES:
        {analysis_report}

        Write a letter that:
        • Starts with professional greeting
        • Focuses on technologies and skills from job requirements
        • Highlights specific relevant experience
        • Is concise (max 200 words), professional and to the point
        • Ends with call to action

        Focus on technical skills and professional experience. Avoid generic phrases.
        {'Focus on revising the previous draft according to the reviewer feedback.' if reviewer_feedback else ''}
        {feedback_section}
        """

        cover_letter = self.llm.invoke(prompt, system_prompt)
        return {
            "draft_cover_letter": cover_letter.strip(),
            "revision_attempts": revision_attempts + 1,
            "needs_revision": False,
            "cover_letter_feedback": "",
        }