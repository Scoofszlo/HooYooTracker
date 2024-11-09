from abc import ABC, abstractmethod
from typing import Dict, List
from bs4 import Tag
from hooyootracker.logger import Logger

logger = Logger.get_logger()


class DataExtractor(ABC):
    def __new__(cls) -> List[Dict[str, str]]:
        instance = super(DataExtractor, cls).__new__(cls)
        instance.__init__()

        logger.debug(f"DataExtractor instance created with code_info: {instance.code_info}")

        return instance.code_info

    def __init__(self, source_name: str, source_url: str) -> None:
        logger.debug(f"Initializing DataExtractor with source_name: {source_name}, source_url: {source_url}")

        self.code_info = {
            "source_name": source_name,
            "source_url": source_url,
            "code_list": self.get_data(source_name, source_url)
        }

        code_list_len = len(self.code_info["code_list"])
        logger.info(f"Data successfully extracted from {source_name} ({code_list_len} codes)")

    def get_data(self, source_name: str, source_url: str) -> List[Dict[str, str]]:
        """Returns a list of dicts containing the code and reward details,
        both in string type"""
        logger.debug(f"Getting data from source_url: {source_url}")
        logger.info(f"Getting data from {source_name} ({source_url})")

        source_data = self._scrape_data(source_url)
        logger.debug(f"Scraped data: {source_data}")

        code_list = []

        for entry in source_data:
            extracted_data = self._extract_data(entry)
            logger.debug(f"Extracted data: {extracted_data}")
            code_list.append(extracted_data)

        return code_list

    @abstractmethod
    def _scrape_data(self, source_url: str) -> List[Tag]:
        """Scrapes data from specified URL source and returns a Tag
        containing list of codes and description"""
        pass

    def _extract_data(self, entry: Tag) -> Dict[str, str]:
        """Extracts the code and reward description from the entry,
        organizing them into dictionary, thus returning it"""
        logger.debug(f"Extracting data from entry: {entry}")

        code = self._get_code(entry)
        reward_desc = self._get_reward_desc(entry)

        logger.debug(f"Extracted code: {code}, reward_desc: {reward_desc}")

        entry_details = {
            "code": code,
            "reward_desc": reward_desc
        }

        return entry_details

    @abstractmethod
    def _get_code(self, entry: Tag) -> str:
        """Extracts the code and return it as a string"""
        pass

    @abstractmethod
    def _get_reward_desc(self, entry: Tag) -> str:
        """Extracts the reward description and return it as a string"""
        pass
