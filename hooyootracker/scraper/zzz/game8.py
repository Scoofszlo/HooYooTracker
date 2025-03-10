import re
import requests
from typing import Optional, Union
from bs4 import BeautifulSoup, ResultSet, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import CodeEntriesList, Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class Game8(Scraper):
    source_name = Source.GAME8
    source_url = SOURCE_URLS[Game.ZENLESS_ZONE_ZERO][source_name]

    def __init__(self):
        self.code_entries_list: CodeEntriesList = CodeEntriesList(
            source_name=self.source_name.value,
            source_url=self.source_url,
            code_list=[]
        )

    def get_data(self):
        return super().get_data()

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> Union[ResultSet, None]:
        response = requests.get(source_url)
        webpage = BeautifulSoup(response.text, 'html.parser')

        code_list = webpage.find('ul', class_='a-list')
        if isinstance(code_list, Tag):
            source_data = code_list.find_all('li')
            return source_data

        return None

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
