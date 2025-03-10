import re
import requests
from typing import Any, Optional, Union
from bs4 import BeautifulSoup, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class Polygon(Scraper):
    source_name = Source.POLYGON
    source_url = SOURCE_URLS[Game.ZENLESS_ZONE_ZERO][source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    def get_data(self):
        return super().get_data()

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> Any:
        response = requests.get(source_url)
        webpage = BeautifulSoup(response.text, 'html.parser')

        list_container = webpage.find('div', class_='_11x6rb9y')
        if list_container is None or not isinstance(list_container, Tag):
            return None

        code_list = list_container.find('ul')
        if code_list is None or not isinstance(code_list, Tag):
            return None

        source_data = code_list.find_all('li')
        return source_data

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> Optional[str]:
        code_tag = entry.find('a')
        if code_tag is None or not isinstance(code_tag, Tag):
            return None

        code = code_tag.text
        return code

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_desc")
    def _get_reward_details(self, entry: Tag) -> Union[str, None]:
        code_and_reward_list_tag = entry.find('span')
        if code_and_reward_list_tag is None or not isinstance(code_and_reward_list_tag, Tag):
            return None

        code_and_reward_list = code_and_reward_list_tag.text
        reward_details = re.split(r"\s+\(", code_and_reward_list)[1]

        return reward_details
