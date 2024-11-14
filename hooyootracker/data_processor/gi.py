from typing import Dict, List, Type
from hooyootracker.scraper.gi import (
    Game8,
    PocketTactics,
    RockPaperShotgun,
    VG247
)
from hooyootracker.logger import Logger
from ._base import DataProcessor

logger = Logger()


class GenshinImpactDP(DataProcessor):
    def get_data(self, sources: List[str]) -> List[Dict[str, str]]:
        source_classes = {
            "PocketTactics": PocketTactics,
            "Game8": Game8,
            "RockPaperShotgun": RockPaperShotgun,
            "VG247": VG247
        }

        final_list = self._get_data_list(
            sources,
            source_classes,
            code_link_template="https://genshin.hoyoverse.com/en/gift?code={code}"
        )

        if final_list:
            logger.info(f"Total list of codes: {len(final_list)}")

        return final_list

    def get_sources(self, config_path: str) -> List[str]:
        source_key = "gi_sources"

        config = super().get_sources(config_path, source_key)

        sources = config['sources'][source_key]
        logger.debug(f"Sources retrieved: {sources}")

        return sources

    def _get_data_list(
            self,
            sources: List[str],
            source_classes: Dict[str, Type],
            code_link_template: str
    ) -> List[Dict[str, str | List]] | None:
        return super()._get_data_list(sources, source_classes, code_link_template)
