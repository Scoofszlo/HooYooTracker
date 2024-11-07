import re
import requests
from bs4 import BeautifulSoup, Tag
from typing import List
from ._source_url import SOURCE_URLS
from ._base import DataExtractor


class Game8(DataExtractor):
    def __init__(self):
        source_name = "Game8"
        source_url = SOURCE_URLS[source_name]
        super().__init__(source_name, source_url)

    def _scrape_data(self, source_url: str) -> List[Tag]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        code_list = webpage.find('ol', class_='a-orderedList')
        source_data = code_list.find_all('li')
        return source_data

    def _get_code(self, entry: Tag) -> str:
        code = entry.find('a').text
        return code

    def _get_reward_desc(self, entry: Tag) -> str:
        code_and_reward_list = entry.text

        reward_desc = re.split(r"\s+-\s+", code_and_reward_list)[1]
        return reward_desc
