from enum import Enum


class Game(Enum):
    GenshinImpact = "Genshin Impact"
    ZenlessZoneZero = "Zenless Zone Zero"


class Source(Enum):
    Game8 = "Game8"
    PocketTactics = "PocketTactics"
    RockPaperShotgun = "RockPaperShotgun"
    VG247 = "VG247"
    Polygon = "Polygon"


# Default sources for Genshin Impact scrapers
DEFAULT_GI_SOURCES = [
    Source.Game8.value,
    Source.PocketTactics.value,
    Source.RockPaperShotgun.value,
    Source.VG247.value
]

# Default sources for Zenless Zone Zero scrapers
DEFAULT_ZZZ_SOURCES = [
    Source.Game8.value,
    Source.PocketTactics.value,
    # Source.Polygon.value,
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
