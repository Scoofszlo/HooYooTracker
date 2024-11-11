import os
import toml
from hooyootracker.logger import Logger
from .constants import (
    PROGRAM_DATA_DIR,
    CONFIG_FILE_PATH,
    DEFAULT_CONFIG
)


def _init_program_data_dir() -> None:
    if not os.path.exists(PROGRAM_DATA_DIR):
        logger.debug("PROGRAM_DATA_DIR doesn't exist. Initializing")

        os.mkdir(PROGRAM_DATA_DIR)

        logger.debug(f"PROGRAM_DATA_DIR created successfully ({os.path.abspath(PROGRAM_DATA_DIR)})")


def _init_file_config() -> None:
    if not os.path.isfile(CONFIG_FILE_PATH):
        logger.debug("CONFIG_FILE doesn't exist. Initializing")

        with open(CONFIG_FILE_PATH, 'w') as file:
            toml.dump(DEFAULT_CONFIG, file)

        logger.debug(f"CONFIG_FILE created successfully ({os.path.abspath(CONFIG_FILE_PATH)})")


def run():
    _init_program_data_dir()
    _init_file_config()


logger = Logger()
run()
