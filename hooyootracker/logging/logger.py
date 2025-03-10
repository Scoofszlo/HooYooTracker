import logging
import logging.handlers
import toml
from typing import Any, Dict
from hooyootracker.constants import CONFIG_FILE_PATH, LOG_DIR


logger: logging.Logger


def init_logger():
    global logger

    # Initialize variables for logger settings
    logger_settings = _get_logger_settings()
    console_handler_level = _identify_console_handler_level(logger_settings)

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")
    logger.propagate = False

    console_handler = logging.StreamHandler()
    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_DIR + "app.log",
        when="midnight",
        backupCount=30,
        utc=True,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "{asctime} [{levelname}] - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S%z"
    )

    console_handler.setLevel(console_handler_level)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def _identify_console_handler_level(logger_settings: Dict[str, Any]) -> int:
    logger_level = logger_settings["debug_level"]
    console_handler_level = logger_level.upper()

    if console_handler_level == "INFO":
        return logging.INFO
    elif console_handler_level == "DEBUG":
        return logging.DEBUG
    elif console_handler_level == "WARNING":
        return logging.WARNING
    elif console_handler_level == "ERROR":
        return logging.ERROR
    elif console_handler_level == "CRITICAL":
        return logging.CRITICAL
    else:
        logging.getLogger(__name__).warning(f"Invalid logging level '{console_handler_level}' provided. Defaulting to INFO.")
        return logging.INFO


def _get_logger_settings() -> Dict[str, Any]:
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = toml.load(file)
    return config["logger"]
