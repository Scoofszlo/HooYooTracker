import re
import requests
from typing import Any, Optional, Union
from bs4 import BeautifulSoup, Tag
from hooyootracker.constants import Game, Source
from hooyootracker.scraper._exceptions.handler import handle_data_extraction_exc, handle_source_exc
from hooyootracker.scraper.scraper import CodeEntriesList, Scraper
from hooyootracker.scraper.source_urls import SOURCE_URLS


class VG247(Scraper):
    source_name = Source.VG247
    source_url = SOURCE_URLS[Game.GENSHIN_IMPACT][source_name]

    def __init__(self):
        self.code_entries_list: CodeEntriesList = CodeEntriesList(
            source_name=self.source_name.value,
            source_url=self.source_url,
            code_list=[]
        )

    def get_data(self):
        return super().get_data()

    @handle_source_exc(source_name=source_name)
    def _get_source_data(self, source_url: str) -> Union[Any, None]:
        response = requests.get(source_url)
        webpage = BeautifulSoup(response.text, 'html.parser')

        list_container = webpage.find('div', class_='article_body_content')
        if isinstance(list_container, Tag):
            code_list = list_container.find_all('ul')[1]
            source_data = code_list.find_all('li')

            return source_data

        return None

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="code")
    def _get_code(self, entry: Tag) -> Optional[str]:
        code = entry.find('strong')
        if isinstance(code, Tag):
            return code.text

        return None

    @handle_data_extraction_exc(source_name=source_name, data_extraction_type="reward_details")
    def _get_reward_details(self, entry: Tag) -> str:
        code_and_reward_list = entry.text

        try:
            reward_desc = re.split(r":\s+", code_and_reward_list)[1]
        except Exception:
            reward_desc = re.split(r"-\s+", code_and_reward_list)[1]

        return reward_desc
