from hooyootracker.extractor.gi import (
    Game8,
    PocketTactics,
    RockPaperShotgun,
    VG247
)
from hooyootracker.logger import Logger

logger = Logger()


def get_data():
    sources = [Game8(), PocketTactics(), RockPaperShotgun(), VG247()]

    unique_list = set()
    final_list = []
    total_duplicate_codes = 0

    logger.info(f"Removing potential duplicate code entries from {len(sources)} sources")

    for source in sources:
        logger.debug(f"Processing source: {source['source_name']}")
        code_list = source['code_list']

        for entry in code_list:
            code = entry["code"]

            if code not in unique_list:
                unique_list.add(code)

                code_info = {
                    "source_name": source["source_name"],
                    "source_url": source["source_url"],
                    "code": code,
                    "reward_desc": entry["reward_desc"],
                    "code_link": f"https://genshin.hoyoverse.com/en/gift?code={code}"
                }

                final_list.append(code_info)
                logger.debug(f"Added new code: {code} from {source['source_name']}")
            else:
                total_duplicate_codes += 1
                logger.debug(f"Duplicate code found: {code} ({source['source_name']})")

    logger.info(f"Removed {total_duplicate_codes} duplicate codes")
    logger.info(f"Total list of codes: {len(final_list)}")

    return final_list
