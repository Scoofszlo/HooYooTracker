import logging
import logging.handlers
import toml
from typing import Any, Dict
from hooyootracker.constants import CONFIG_FILE_PATH, LOG_DIR


class Logger:
    _instance = None

    def __new__(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__init__(cls)
        return cls._instance.logger

    def __init__(self, cls):
        if not hasattr(self, 'logger'):
            # Initialize variables for logger settings
            logger_settings = cls._get_logger_settings()
            console_handler_level = cls._identify_console_handler_level(logger_settings)

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel("DEBUG")
            self.logger.propagate = False

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

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    @staticmethod
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

    @staticmethod
    def _get_logger_settings() -> Dict[str, Any]:
        with open(CONFIG_FILE_PATH, 'r') as file:
            config = toml.load(file)
        return config["logger"]
