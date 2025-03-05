import re
import requests
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class Game8(Scraper):
    source_name = Source.Game8
    source_url = SOURCE_URLS[Game.ZenlessZoneZero][source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    def get_data(self):
        return super().get_data(self.source_name, self.source_url)

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> List[Tag]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        code_list = webpage.find('ul', class_='a-list')
        source_data = code_list.find_all('li')

        return source_data

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> Optional[str]:
        code_and_reward_list = entry.text

        code = re.split(r"\s+-\s+", code_and_reward_list)[0]
        return code

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_desc")
    def _get_reward_details(self, entry: Tag) -> Optional[str]:
        code_and_reward_list = entry.text

        reward_details = re.split(r"\s+-\s+", code_and_reward_list)[1]
        return reward_details
