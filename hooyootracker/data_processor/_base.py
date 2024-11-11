import toml
from abc import abstractmethod
from typing import Any, Dict, List, Type
from hooyootracker.exceptions.data_processor import FileParsingError
from hooyootracker.logger import Logger

logger = Logger()


class BaseDataProcessor:
    @abstractmethod
    def get_data(self, sources: List[str]) -> List[Dict[str, str]]:
        """
        Process data based from specified sources and returns it with a list
        of codes and its reward details
        """

    @abstractmethod
    def get_sources(self, config_path: str, source_key: str) -> Dict[str, Any]:
        """
        Retrieves a list of source names specified from the config path and returns a
        list of strings containing source names.

        If there is an error parsing the config file, it will return a None
        and nothing will be processed.
        """

        logger.debug(f"Attempting to open config file at: {config_path}")

        try:
            with open(config_path, 'r') as file:
                config = toml.load(file)
            logger.debug("Config file loaded successfully")
            return config
        except Exception as e:
            logger.critical(f"Error parsing config file: {e}", exc_info=True)
            raise FileParsingError from e

    def _get_data_list(self, sources: List[str], source_classes: Dict[str, Type], code_link_template: str) -> List[Dict[str, str | List]] | None:
        if sources is None:
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

        clean_list = self._remove_duplicate_entries(info_list, code_link_template)

        return clean_list

    def _remove_duplicate_entries(self, sources: List[Dict[str, str | List]], code_link_template: str) -> List[Dict[str, str]]:
        if sources is None:
            return None

        clean_list = []

        if len(sources) == 1:
            for source in sources:
                if not source['code_list']:
                    return None

                for entry in source['code_list']:
                    code = entry["code"]

                    code_info = self._get_code_info(source, entry, code_link_template, code)
                    clean_list.append(code_info)

        elif len(sources) >= 2:
            unique_list = set()
            total_duplicate_codes = 0

            logger.info(f"Removing potential duplicate code entries from {len(sources)} sources")

            for source in sources:
                logger.debug(f"Processing source: {source['source_name']}")

                if not source['code_list']:
                    continue

                for entry in source['code_list']:
                    code = entry["code"]

                    if code not in unique_list:
                        unique_list.add(code)

                        code_info = self._get_code_info(source, entry, code_link_template, code)

                        clean_list.append(code_info)
                        logger.debug(f"Skipping {code} ({source['source_name']}) as it is unique")
                    else:
                        total_duplicate_codes += 1
                        logger.debug(f"Duplicate code found: {code} ({source['source_name']})")

            logger.info(f"Removed {total_duplicate_codes} duplicate codes")

        return clean_list

    def _get_code_info(self, source, entry, code_link_template, code):
        code_info = {
            "source_name": source["source_name"],
            "source_url": source["source_url"],
            "code": code,
            "reward_desc": entry["reward_desc"],
            "code_link": code_link_template.format(code=code)
        }

        return code_info
