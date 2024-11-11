# Default sources for Genshin Impact scrapers
DEFAULT_GI_SOURCES = [
    "Game8",
    "PocketTactics",
    "RockPaperShotgun",
    "VG247"
]

# Default sources for Zenless Zone Zero scrapers
DEFAULT_ZZZ_SOURCES = [
    "Game8",
    "PocketTactics",
    "Polygon",
    "VG247"
]


# Directory for storing program data
PROGRAM_DATA_DIR = "program_data"
# Path to the configuration file
CONFIG_FILE_PATH = PROGRAM_DATA_DIR + "/config.toml"

# Default configuration settings
DEFAULT_CONFIG = {
    "sources": {
        "gi_sources": DEFAULT_GI_SOURCES,
        "zzz_sources": DEFAULT_ZZZ_SOURCES
    }
}
