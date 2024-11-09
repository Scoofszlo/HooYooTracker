import logging


class Logger:
    _instance = None

    def __new__(cls, level="INFO"):
        if cls._instance is None:
            level = cls.identify_level(level)
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__init__(level)
        return cls._instance.logger

    def __init__(self, level):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(level)
            self.logger.propagate = False
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "{asctime} [{levelname}] - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M:%S%z")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    @staticmethod
    def identify_level(level):
        level = level.upper()
        if level == "INFO":
            return logging.INFO
        elif level == "DEBUG":
            return logging.DEBUG
        elif level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        elif level == "CRITICAL":
            return logging.CRITICAL
        else:
            logging.getLogger(__name__).warning(f"Invalid logging level '{level}' provided. Defaulting to INFO.")
            return logging.INFO
