from langgraph.graph import StateGraph
from typing import Dict, Any
from custom_llm import CustomLLM

class VacancyAnalyzerAgent:
    def __init__(self, llm: CustomLLM):
        self.llm = llm
        
    def analyze_vacancy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        vacancy_text = state["vacancy_description"]
        
        system_prompt = """You are an experienced HR analyst. Your task is to thoroughly analyze job descriptions 
        and identify key requirements, skills, and company specifics. Pay attention to details."""
        
        prompt = f"""
        Analyze the job description and identify ALL key elements:

        JOB DESCRIPTION:
        {vacancy_text}

        RETURN RESPONSE IN THE FORMAT:
        - Position: [job title]
        - Key responsibilities: [list of responsibilities]
        - Required skills: [list of skills]
        - Preferred skills: [list of skills] 
        - Required experience: [experience level]
        - Language level: [if specified]
        - Company/project specifics: [what stands out]
        - Technology stack: [technologies and tools]
        """
        
        analysis = self.llm.invoke(prompt, system_prompt)
        return {"vacancy_analysis": analysis}
    
    def analyze_resume(self, state: Dict[str, Any]) -> Dict[str, Any]:
        resume_text = state["resume"]
        
        system_prompt = """You are a professional HR expert. Analyze candidate resumes, 
        highlighting their key competencies, experience, and achievements. Be objective and attentive."""
        
        prompt = f"""
        Analyze the candidate's resume:

        RESUME:
        {resume_text}

        RETURN RESPONSE IN THE FORMAT:
        - Key skills: [list of main skills]
        - Work experience: [overall experience and key positions]
        - Achievements: [specific results and achievements]
        - Education: [education and certificates]
        - Language level: [if specified]
        - Strengths: [what distinguishes the candidate]
        - Projects: [key projects if available]
        """
        
        analysis = self.llm.invoke(prompt, system_prompt)
        return {"resume_analysis": analysis}
        
    def create_match_report(self, state: Dict[str, Any]) -> Dict[str, Any]:
        vacancy_analysis = state.get("vacancy_analysis", "")
        resume_analysis = state.get("resume_analysis", "")
        
        system_prompt = """You are a recruitment expert. Compare job requirements 
        and candidate competencies to create an objective and useful report for composing 
        a cover letter. Be specific and provide practical recommendations."""
        
        prompt = f"""
        Based on the analysis of the vacancy and resume, create a DETAILED REPORT for the cover letter generator.

        VACANCY ANALYSIS:
        {vacancy_analysis}

        RESUME ANALYSIS:
        {resume_analysis}

        CREATE THE REPORT IN THE FOLLOWING FORMAT:

        ## STRONG SIDES (perfect match):
        - [specific skill/experience from resume] → [corresponding job requirement]
        - [another matching point]

        ## GROWTH AREAS (partial match):
        - [skill that exists but needs development] → [job requirement]
        - [experience that can be presented differently]

        ## GAPS (missing requirements):
        - [what is missing in the resume] → [job requirement]

        ## RECOMMENDATIONS FOR COVER LETTER:
        ### What to emphasize:
        - [specific points to highlight]
        
        ### How to compensate for gaps:
        - [strategies to explain missing skills]
        
        ### Keywords to use:
        - [words and phrases from the vacancy]
        
        ### Letter tone:
        - [recommended tone: confident/enthusiastic/professional]
        """
        
        report = self.llm.invoke(prompt, system_prompt)
        return {"analysis_report": report}