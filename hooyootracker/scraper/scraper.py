from abc import abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from bs4 import Tag
from hooyootracker.constants import Source
from hooyootracker.logger import Logger

logger = Logger()


@dataclass
class CodeEntry:
    code: str
    reward_details: str


@dataclass
class CodeEntriesList:
    source_name: str
    source_url: str
    code_list: List[CodeEntry]


class Scraper:
    def __init__(self, source_name: Source, source_url: str):
        self.code_entries_list: CodeEntriesList = CodeEntriesList(
            source_name=source_name.value,
            source_url=source_url,
            code_list=[]
        )

    def get_data(self) -> Optional[CodeEntriesList]:
        source_name = self.code_entries_list.source_name
        source_url = self.code_entries_list.source_url

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
                self.code_entries_list.code_list.append(extracted_data)
                success_ctr += 1
            else:
                continue

        logger.debug(f"Extracted {success_ctr}/{len(source_data)} entries from {source_name}")

        return self.code_entries_list

    @abstractmethod
    def _get_source_data(self, source_url: str) -> Optional[List[Tag]]:
        """Scrapes source data from specified URL source and returns a list of Tags
        containing codes and reward details"""
        pass

    def _extract_data(self, item: Tag) -> Optional[CodeEntry]:
        """Extracts the code and reward description from the entry,
        organizing them into a CodeEntry dataclass, thus returning it"""
        logger.debug(f"Extracting data from entry: {item}")

        code = self._get_code(item)
        reward_details = self._get_reward_details(item)

        if not code or not reward_details:
            return

        entry_details = CodeEntry(code, reward_details)

        logger.debug(f"Extracted info: {entry_details}")

        return entry_details

    @abstractmethod
    def _get_code(self, entry: Tag) -> Optional[str]:
        """Extracts the code and returns it as a string."""
        pass

    @abstractmethod
    def _get_reward_details(self, entry: Tag) -> Optional[str]:
        """Extracts the reward details and returns it as a string"""
        pass
