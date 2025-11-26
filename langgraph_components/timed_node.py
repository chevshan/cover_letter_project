from app.core.config import logger
import time

def timed_node(node_name: str, fn):
    def wrapper(state):
        start = time.perf_counter()
        logger.info("Node %s: start", node_name)
        try:
            result = fn(state)
            return result
        finally:
            duration = time.perf_counter() - start
            logger.info("Node %s: finished in %.3f s", node_name, duration)
    return wrapper