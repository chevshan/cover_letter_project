from typing import Dict, Any
from app.core.config import logger
import time

def generate_cover_letter(vacancy: str, resume: str, workflow) -> Dict[str, Any]:
    initial_state = {
        "vacancy_description": vacancy,
        "resume": resume,
        "revision_attempts": 0,
        "needs_revision": False,
        "cover_letter_feedback": "",
    }

    start = time.perf_counter()
    logger.info("Workflow start")
    try:
        result = workflow.invoke(initial_state)
        return result
    finally:
        duration = time.perf_counter() - start
        logger.info("Workflow finished in %.3f s", duration)