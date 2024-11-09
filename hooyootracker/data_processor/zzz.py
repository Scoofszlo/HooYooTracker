from typing import Dict, List
from hooyootracker.extractor.zzz import (
    Game8
)
from hooyootracker.logger import Logger

logger = Logger()


def get_data() -> List[Dict[str, str]]:
    info_set = get_data_list()
    final_list = remove_duplicate_entries(info_set)

    logger.info(f"Total list of codes: {len(final_list)}")

    return final_list


def get_data_list() -> List[Dict[str, str | List]]:
    info_list = [Game8()]

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
