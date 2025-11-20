from typing import Dict, Any

def generate_cover_letter(vacancy: str, resume: str, workflow) -> Dict[str, Any]:
    initial_state = {
        "vacancy_description": vacancy,
        "resume": resume
    }

    return workflow.invoke(initial_state)