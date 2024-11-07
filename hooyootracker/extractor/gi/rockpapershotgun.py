import re
import requests
from bs4 import BeautifulSoup, Tag
from typing import List
from ._source_url import SOURCE_URLS
from ._base import DataExtractor


class RockPaperShotgun(DataExtractor):
    def __init__(self):
        source_name = "RockPaperShotgun"
        source_url = SOURCE_URLS[source_name]
        super().__init__(source_name, source_url)

    def _scrape_data(self, source_url: str) -> List[Tag]:
        webpage = requests.get(source_url)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        list_container = webpage.find('div', class_='article_body_content')
        code_list = list_container.find_all('ul')[1]
        source_data = code_list.find_all('li')

        return source_data

    def _get_code(self, entry: Tag) -> str:
        code = entry.find('strong').text
        return code

    def _get_reward_desc(self, entry: Tag) -> str:
        code_and_reward_list = entry.text
        
        reward_desc = re.split(r":\s+", code_and_reward_list)[1]
        return reward_desc
