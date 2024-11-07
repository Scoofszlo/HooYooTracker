import logging


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.propagate = False
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "{asctime} [{levelname}] - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M:%S%z")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    @staticmethod
    def get_logger(level="INFO"):
        level = level.upper()
        if level == "INFO":
            level = logging.INFO
        elif level == "DEBUG":
            level = logging.DEBUG
        elif level == "WARNING":
            level = logging.WARNING
        elif level == "ERROR":
            level = logging.ERROR
        elif level == "CRITICAL":
            level = logging.CRITICAL
        else:
            level = logging.INFO
            Logger().logger.warning(f"Invalid logging level '{level}' provided. Defaulting to INFO.")

        logger_instance = Logger().logger
        logger_instance.setLevel(level)
        return logger_instance
