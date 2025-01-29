from abc import abstractmethod
from typing import Dict, List, Optional
from bs4 import Tag
from hooyootracker.logger import Logger

logger = Logger()


class Scraper:
    def __init__(self, source_name: str, source_url: str):
        self.code_entries_list: Dict[str, str | List] = {
            "source_name": source_name,
            "source_url": source_url,
            "code_list": []
        }

    def get_data(self, source_name: str, source_url: str):
        logger.info(f"Getting data from {source_name} ({source_url})")

        # Extracts the data from source that has the container containing
        # the code and its reward details, which then returns a list of Tags
        source_data = self._get_source_data(source_url)

        if not source_data:
            return
        else:
            logger.debug(f"Scraped source data: {source_data}")

        # Start extraction of data
        success_ctr = 0

        for item in source_data:
            extracted_data = self._extract_data(item)
            if extracted_data:
                self.code_entries_list["code_list"].append(extracted_data)
                success_ctr += 1
            else:
                continue

        logger.debug(f"Extracted {success_ctr}/{len(source_data)} entries from {source_name}")

        return self.code_entries_list

    @abstractmethod
    def _get_source_data(self, source_url: str) -> Optional[List[Tag]]:
        """Scrapes source data from specified URL source and returns a Tag
        containing list of codes and reward details"""
        pass

    def _extract_data(self, item: Tag) -> Optional[Dict[str, str]]:
        """Extracts the code and reward description from the entry,
        organizing them into dictionary, thus returning it"""
        logger.debug(f"Extracting data from entry: {item}")

        code = self._get_code(item)
        reward_details = self._get_reward_details(item)

        if not code or not reward_details:
            return

        entry_details = {
            "code": code,
            "reward_details": reward_details
        }

        logger.debug(f"Extracted info: {entry_details}")

        return entry_details

    @abstractmethod
    def _get_code(self, entry: Tag) -> str:
        """Extracts the code and return it as a string"""
        pass

    @abstractmethod
    def _get_reward_details(self, entry: Tag) -> str:
        """Extracts the reward details and return it as a string"""
        pass
