from typing import Dict, Any
from custom_llm import CustomLLM

class CopyWriterAgent:
    def __init__(self, llm: CustomLLM):
        self.llm = llm
    
    def generate_cover_letter(self, state: Dict[str, Any]) -> Dict[str, Any]:
        analysis_report = state.get("analysis_report", "")
        vacancy_description = state.get("vacancy_description", "")
        resume = state.get("resume", "")

        system_prompt = """You are an expert copywriter specializing in cover letters. 
        Create compelling, professional cover letters that are ready to send.
        
        IMPORTANT: Return ONLY the cover letter text, without any:
        - Analysis reports
        - Explanations
        - Markdown formatting
        - Section headers like "Cover Letter"
        - Additional comments
        
        The output should be a clean, professional letter that can be directly copied and sent to employers."""

        prompt = f"""
        Based on the analysis below, write a professional cover letter that is ready to send immediately.

        JOB DESCRIPTION:
        {vacancy_description}

        CANDIDATE BACKGROUND:
        {resume}

        ANALYSIS INSIGHTS:
        {analysis_report}

        Write a compelling cover letter that:
        1. Starts with professional salutation
        2. Highlights the candidate's most relevant skills and experience for this specific position
        3. Shows enthusiasm for the company/role
        4. Ends with professional closing and call to action
        5. Is tailored, professional, and ready to send

        Format it as a proper business letter without any additional explanations or markdown.
        """

        cover_letter = self.llm.invoke(prompt, system_prompt)
        return {"cover_letter": cover_letter}