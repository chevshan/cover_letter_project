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

        Focus on technical skills and professional experience. Avoid generic phrases.
        {'Focus on revising the previous draft according to the reviewer feedback.' if reviewer_feedback else ''}
        {feedback_section}
        The final letter of recommendation should be such that the user can immediately send it to the employer, take this into account and do not write anything superfluous.

        Example:
        [Name]

        Dear Hiring Manager,

        I am writing to express my strong interest in the Software Engineer position at Innovate Solutions Inc., as advertised on your careers page. With a solid foundation in full-stack development, experience building scalable web applications, and a passion for solving real-world problems through technology, I am confident in my ability to contribute effectively to your engineering team.

        During my recent role at TechStart Labs, I developed and deployed a React-based dashboard that reduced client onboarding time by 30%. I collaborated closely with product and data teams to integrate RESTful APIs and implemented CI/CD pipelines using GitHub Actions—practices I understand your team values highly. I also optimized backend performance in Python (FastAPI), cutting average response latency by 40%.

        What excites me most about Innovate Solutions is your commitment to ethical AI and user-centric design—principles that align with my own professional values. I admire your recent work on the OpenAccess platform, and I would be honored to help extend its impact through clean, maintainable code and thoughtful engineering.

        Thank you for considering my application. I welcome the opportunity to discuss how my skills and enthusiasm can support your team’s goals. I am available at your convenience for an interview and can be reached at the contact information above.

        Sincerely,
        [Name]
        """

        cover_letter = self.llm.invoke(prompt, system_prompt)
        return {
            "draft_cover_letter": cover_letter.strip(),
            "revision_attempts": revision_attempts + 1,
            "needs_revision": False,
            "cover_letter_feedback": "",
        }