from enum import Enum


class Game(Enum):
    GENSHIN_IMPACT = "Genshin Impact"
    ZENLESS_ZONE_ZERO = "Zenless Zone Zero"


class Source(Enum):
    GAME8 = "Game8"
    POCKET_TACTICS = "Pocket Tactics"
    ROCK_PAPER_SHOTGUN = "Rock Paper Shotgun"
    VG247 = "VG247"
    POLYGON = "Polygon"


# Default sources for Genshin Impact scrapers
DEFAULT_GI_SOURCES = [
    Source.GAME8.value,
    Source.POCKET_TACTICS.value,
    Source.ROCK_PAPER_SHOTGUN.value,
    Source.VG247.value
]

# Default sources for Zenless Zone Zero scrapers
DEFAULT_ZZZ_SOURCES = [
    Source.GAME8.value,
    Source.POCKET_TACTICS.value,
    # Source.POLYGON.value,
    Source.VG247.value
]


# Directory for storing program data
PROGRAM_DATA_DIR = "program_data"
# Path to the configuration file
CONFIG_FILE_PATH = PROGRAM_DATA_DIR + "/config.toml"
# Directory for logs
LOG_DIR = PROGRAM_DATA_DIR + "/logs/"
# Directory for database
DB_FILE_PATH = PROGRAM_DATA_DIR + "/data.db"

# Default configuration settings
DEFAULT_CONFIG = {
    "sources": {
        "gi_sources": DEFAULT_GI_SOURCES,
        "zzz_sources": DEFAULT_ZZZ_SOURCES
    },
    "logger": {
        "debug_level": "INFO"
    }
}
