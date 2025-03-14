import logging
import logging.handlers
from hooyootracker.config.config import Config
from hooyootracker.constants import LOG_DIR


logger: logging.Logger
config = Config()


def init_logger():
    global logger

    console_handler_level = _identify_console_handler_level()

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


def _identify_console_handler_level() -> int:
    logger_level = config.get_log_level()
    console_handler_level = logger_level.upper()

    log_levels = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    if console_handler_level in log_levels:
        return log_levels[console_handler_level]
    else:
        logging.getLogger(__name__).warning(f"Invalid logging level '{console_handler_level}' provided. Defaulting to INFO.")
        return logging.INFO
