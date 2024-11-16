from abc import ABC, abstractmethod
from bs4 import Tag
from typing import Any, Dict, List, Optional
from hooyootracker.logger import Logger

logger = Logger()


class DataExtractor(ABC):
    def __new__(cls) -> Dict[str, str | List]:
        instance = super(DataExtractor, cls).__new__(cls)
        instance.__init__()

        return instance.code_info

    def __init__(self, source_name: str, source_url: str) -> None:
        self.code_info: Dict[str, Any] = {}
        self.get_data(source_name, source_url)

    def get_data(self, source_name: str, source_url: str) -> None:
        """
        Returns a list of dicts containing the code and reward details,
        both in string type
        """

        logger.info(f"Getting data from {source_name} ({source_url})")

        source_data = self._get_source_data(source_url)
        if not source_data:
            return

        logger.debug(f"Scraped source data: {source_data}")

        logger.debug(f"Extracting {len(source_data)} entries from {source_name}")

        code_list = []
        success_ctr = 0
        failed_ctr = 0
        for entry in source_data:
            extracted_data = self._extract_data(entry)

            if extracted_data:
                code_list.append(extracted_data)
                success_ctr += 1
            else:
                failed_ctr += 1
                continue

        self.code_info = {
            "source_name": source_name,
            "source_url": source_url,
            "code_list": code_list
        }

        logger.debug(f"Extracted {success_ctr-failed_ctr}/{success_ctr} entries from {source_name}")

    @abstractmethod
    def _get_source_data(self, source_url: str) -> Optional[List[Tag]]:
        """Scrapes source data from specified URL source and returns a Tag
        containing list of codes and description"""
        pass

    def _extract_data(self, entry: Tag) -> Dict[str, str]:
        """Extracts the code and reward description from the entry,
        organizing them into dictionary, thus returning it"""
        logger.debug(f"Extracting data from entry: {entry}")

        code = self._get_code(entry)
        reward_desc = self._get_reward_desc(entry)

        if not code or not reward_desc:
            return None

        entry_details = {
            "code": code,
            "reward_desc": reward_desc
        }

        logger.debug(f"Extracted info: {entry_details}")

        return entry_details

    @abstractmethod
    def _get_code(self, entry: Tag) -> str:
        """Extracts the code and return it as a string"""
        pass

    @abstractmethod
    def _get_reward_desc(self, entry: Tag) -> str:
        """Extracts the reward description and return it as a string"""
        pass
