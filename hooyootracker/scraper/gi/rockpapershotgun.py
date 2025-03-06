import re
import requests
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class RockPaperShotgun(Scraper):
    source_name = Source.RockPaperShotgun
    source_url = SOURCE_URLS[Game.GenshinImpact][source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    def get_data(self):
        return super().get_data()

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> Optional[List[Tag]]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        list_container = webpage.find('div', class_='article_body_content')
        code_list = list_container.find_all('ul')[1]
        source_data = code_list.find_all('li')

        return source_data

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> str:
        code = entry.find('strong').text

        return code

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_details")
    def _get_reward_details(self, entry: Tag) -> str:
        code_and_reward_list = entry.text
        reward_desc = re.split(r":\s+", code_and_reward_list)[1]

        return reward_desc
