import toml
from typing import Dict, List
from hooyootracker.extractor.zzz import (
    Game8,
    PocketTactics,
    Polygon,
    VG247
)
from hooyootracker.logger import Logger

logger = Logger()


def get_data(sources: List[str]) -> List[Dict[str, str]]:
    info_set = get_data_list(sources)
    final_list = remove_duplicate_entries(info_set)

    logger.info(f"Total list of codes: {len(final_list)}")

    return final_list


def get_sources(config_path: str) -> List[str] | None:
    """
    Retrieves source names specified from the config path and returns a
    list of strings containing source names.

    If there is an error parsing the config file, it will return a None
    and nothing will be processed.
    """
    logger.debug(f"Attempting to open config file at: {config_path}")

    try:
        with open(config_path, 'r') as file:
            config = toml.load(file)
        logger.debug("Config file loaded successfully")
    except Exception:
        logger.error("Error parsing config file. Nothing will be processed")
        return None

    sources = config['sources']['zzz_sources']
    logger.debug(f"Sources retrieved: {sources}")

    return sources


def get_data_list(sources: List[str]) -> List[Dict[str, str | List]]:
    source_classes = {
        "PocketTactics": PocketTactics,
        "Game8": Game8,
        "Polygon": Polygon,
        "VG247": VG247
    }

    if len(sources) == 0:
        logger.info("No list of sources have been passed. Nothing will be processed.")
        return None
    else:
        logger.info(f"Processing {len(sources)} source{'s' if len(sources) > 1 else ''}")

    info_list = []

    for source in sources:
        if source in source_classes:
            info_list.append(source_classes[source]())
        else:
            logger.info(f"\"{source}\" does not exist in available scrapers. Skipping.")

    return info_list


def remove_duplicate_entries(sources: List[Dict[str, str | List]]) -> List[Dict[str, str]]:
    unique_list = set()
    final_list = []
    total_duplicate_codes = 0

    logger.info(f"Removing potential duplicate code entries from {len(sources)} sources")

    for source in sources:
        logger.debug(f"Processing source: {source['source_name']}")
        code_list = source['code_list']

        if not code_list:
            continue

        for entry in code_list:
            code = entry["code"]

            if code not in unique_list:
                unique_list.add(code)

                code_info = {
                    "source_name": source["source_name"],
                    "source_url": source["source_url"],
                    "code": code,
                    "reward_desc": entry["reward_desc"],
                    "code_link": f"https://zenless.hoyoverse.com/redemption?code={code}"
                }

                final_list.append(code_info)
                logger.debug(f"Skipping {code} ({source['source_name']}) as it is unique")
            else:
                total_duplicate_codes += 1
                logger.debug(f"Duplicate code found: {code} ({source['source_name']})")

    logger.info(f"Removed {total_duplicate_codes} duplicate codes")

    return final_list
