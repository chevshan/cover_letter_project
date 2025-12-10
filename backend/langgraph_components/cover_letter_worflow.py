from agents.vacancy_analyzer_agent import VacancyAnalyzerAgent
from agents.copywriter_agent import CopyWriterAgent
from agents.critic_agent import CriticAgent
from custom_llm import CustomLLM
from langgraph_components.cover_letter_state import CoverLetterState
from langgraph.graph import StateGraph
from langgraph_components.timed_node import timed_node

def create_workflow():
    llm = CustomLLM()

    analyzer_agent = VacancyAnalyzerAgent(llm=llm)
    copywriter_agent = CopyWriterAgent(llm=llm)
    critic_agent = CriticAgent(llm=llm)

    workflow = StateGraph(CoverLetterState)

    workflow.add_node(
        "bootstrap", timed_node("bootstrap", lambda state: {})
    )

    workflow.add_node(
        "analyze_vacancy", timed_node("analyze_vacancy", analyzer_agent.analyze_vacancy)
    )
    workflow.add_node(
        "analyze_resume", timed_node("analyze_resume", analyzer_agent.analyze_resume)
    )
    workflow.add_node(
        "create_report", timed_node("create_report", analyzer_agent.create_match_report)
    )
    workflow.add_node(
        "generate_cover_letter", timed_node("generate_cover_letter", copywriter_agent.generate_cover_letter)
    )
    workflow.add_node(
        "review_cover_letter", timed_node("review_cover_letter", critic_agent.review_cover_letter)
    )
    workflow.add_node(
        "finalize_cover_letter",
        timed_node("finalize_cover_letter", lambda state: {
            "cover_letter": state.get("cover_letter") or state.get("draft_cover_letter", "")
        })
    )

    workflow.set_entry_point("bootstrap")
    workflow.add_edge("bootstrap", "analyze_vacancy")
    workflow.add_edge("bootstrap", "analyze_resume")
    workflow.add_edge("analyze_vacancy", "create_report")
    workflow.add_edge("analyze_resume", "create_report")
    workflow.add_edge("create_report", "generate_cover_letter")
    workflow.add_edge("generate_cover_letter", "review_cover_letter")
    workflow.add_conditional_edges(
        "review_cover_letter",
        lambda state: "revise" if state.get("needs_revision") else "finalize",
        {
            "revise": "generate_cover_letter",
            "finalize": "finalize_cover_letter",
        }
    )
    workflow.set_finish_point("finalize_cover_letter")

    return workflow.compile()