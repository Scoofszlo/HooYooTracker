import re
import requests
from typing import List
from bs4 import BeautifulSoup, Tag
from hooyootracker.scraper_v2._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper_v2.model import Scraper
from hooyootracker.scraper_v2.source_urls import SOURCE_URLS


class PocketTactics(Scraper):
    source_name = "PocketTactics"
    source_url = SOURCE_URLS["zzz"][source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    def get_data(self):
        return super().get_data(self.source_name, self.source_url)

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> List[Tag]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        list_container = webpage.find('div', class_='entry-content')
        code_list = list_container.find('ul')
        source_data = code_list.find_all('li')

        return source_data

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> str:
        code = entry.find('strong').text

        return code

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_desc")
    def _get_reward_details(self, entry: Tag) -> str:
        code_and_reward_list = entry.text
        reward_details = re.split(r"\s+–\s+", code_and_reward_list)[1]

        return reward_details
