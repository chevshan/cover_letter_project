from agents.vacancy_analyzer_agent import VacancyAnalyzerAgent
from agents.copywriter_agent import CopyWriterAgent
from custom_llm import CustomLLM
from langgraph_components.cover_letter_state import CoverLetterState
from langgraph.graph import StateGraph

def create_workflow():
    llm = CustomLLM()

    analyzer_agent = VacancyAnalyzerAgent(llm=llm)
    copywriter_agent = CopyWriterAgent(llm=llm)

    workflow = StateGraph(CoverLetterState)

    workflow.add_node("analyze_vacancy", analyzer_agent.analyze_vacancy)
    workflow.add_node("analyze_resume", analyzer_agent.analyze_resume)
    workflow.add_node("create_report", analyzer_agent.create_match_report)
    workflow.add_node("generate_cover_letter", copywriter_agent.generate_cover_letter)

    workflow.set_entry_point("analyze_vacancy")
    workflow.add_edge("analyze_vacancy", "analyze_resume")
    workflow.add_edge("analyze_resume", "create_report")
    workflow.add_edge("create_report", "generate_cover_letter")
    workflow.set_finish_point("generate_cover_letter")

    return workflow.compile()