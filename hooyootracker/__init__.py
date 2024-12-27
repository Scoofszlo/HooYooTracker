import os
import toml
from .constants import (
    PROGRAM_DATA_DIR,
    CONFIG_FILE_PATH,
    LOG_DIR,
    DB_FILE_PATH,
    DEFAULT_CONFIG
)


def _init_program_data_dir() -> None:
    if not os.path.exists(PROGRAM_DATA_DIR):
        os.mkdir(PROGRAM_DATA_DIR)


def _init_file_config() -> None:
    if not os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as file:
            toml.dump(DEFAULT_CONFIG, file)


def _init_log_dir() -> None:
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)


def _init_db() -> None:
    if not os.path.isfile(DB_FILE_PATH):
        with open(DB_FILE_PATH, 'w'):
            pass


def run():
    _init_program_data_dir()
    _init_file_config()
    _init_log_dir()
    _init_db()


run()
