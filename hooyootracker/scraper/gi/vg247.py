import re
import requests
from bs4 import BeautifulSoup, Tag
from typing import List
from hooyootracker.scraper._exceptions.handler import (
    handle_source_exc,
    handle_data_extraction_exc
)
from ._source_url import SOURCE_URLS
from ._base import DataExtractor


class VG247(DataExtractor):
    source_name = "VG247"
    source_url = SOURCE_URLS[source_name]

    def __init__(self):
        super().__init__(self.source_name, self.source_url)

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> List[Tag]:
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

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_desc")
    def _get_reward_desc(self, entry: Tag) -> str:
        code_and_reward_list = entry.text

        try:
            reward_desc = re.split(r":\s+", code_and_reward_list)[1]
        except Exception:
            reward_desc = re.split(r"-\s+", code_and_reward_list)[1]
        return reward_desc
