import re
import requests
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class PocketTactics(Scraper):
    source_name = Source.PocketTactics
    source_url = SOURCE_URLS[Game.GenshinImpact][source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    def get_data(self):
        return super().get_data()

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> Optional[List[Tag]]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        list_container = webpage.find('div', class_='entry-content')
        code_list = self._process_multiple_lists(list_container)

        source_data = []
        for sublist in code_list:
            for item in sublist.find_all('li'):
                source_data.append(item)

        return source_data

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> str:
        try:
            code = entry.find('strong').text
        except AttributeError:
            code = entry.find('b').text

        return code

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_details")
    def _get_reward_details(self, entry: Tag) -> str:
        code_and_reward_list = entry.text
        reward_details = re.split(r"\s+–\s+", code_and_reward_list)[1]

        return reward_details

    # Classes below are necessary when the base class for data scraping is
    # not enough
    def _process_multiple_lists(self, list_container: Tag) -> List[Tag]:
        first_code_list = list_container.find_all('ul')[0]
        # second_code_list = list_container.find_all('ul')[1]

        code_list = [first_code_list]
        # code_list = [first_code_list, second_code_list]
        return code_list
