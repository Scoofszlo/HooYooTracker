import logging
import logging.handlers
from hooyootracker.constants import LOG_DIR


class Logger:
    _instance = None

    def __new__(cls, console_handler_level: str = "INFO") -> logging.Logger:
        if cls._instance is None:
            console_handler_level = cls.identify_console_handler_level(console_handler_level)
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__init__(console_handler_level)
        return cls._instance.logger

    def __init__(self, console_handler_level: int):
        if not hasattr(self, 'logger'):
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
    def identify_console_handler_level(console_handler_level: str) -> int:
        console_handler_level = console_handler_level.upper()

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
