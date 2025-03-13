from typing import Any, Dict, List
import toml
from hooyootracker.config.exceptions import FileParsingError
from hooyootracker.constants import CONFIG_FILE_PATH
from hooyootracker.logging.logger import logger


class Config:
    _instance = None

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.raw_config = self._load_config()

    def get_sources(self, source_key: str) -> List[str]:
        return self.raw_config['sources'][source_key]

    def _load_config(self) -> Dict[str, Any]:
        """
        This parses the config file specified from the path and loads it.
        If there is an error parsing the config file, this will result in
        exception, thus halting the program.
        """

        logger.debug(f"Attempting to open config file at: {CONFIG_FILE_PATH}")

        try:
            with open(CONFIG_FILE_PATH, 'r') as file:
                config = toml.load(file)
                logger.debug("Config file loaded successfully")
                logger.debug(f"Config data: {config}")
                return config

        except Exception as e:
            logger.critical(f"Error parsing config file: {e}", exc_info=True)
            raise FileParsingError from e
