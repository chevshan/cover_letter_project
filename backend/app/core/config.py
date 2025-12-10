import logging
import os


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGER_NAME = "cover_letter_api"


def configure_logging() -> logging.Logger:
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    return logging.getLogger(LOGGER_NAME)


logger = configure_logging()