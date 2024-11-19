from typing import Dict, List, Type
from hooyootracker.scraper.zzz import (
    Game8,
    PocketTactics,
    Polygon,
    VG247
)
from hooyootracker.logger import Logger
from ._base import DataProcessor

logger = Logger()


class ZenlessZoneZeroDP(DataProcessor):
    def get_data(self, sources: List[str]) -> List[Dict[str, str]]:
        source_classes = {
            "PocketTactics": PocketTactics,
            "Game8": Game8,
            "Polygon": Polygon,
            "VG247": VG247
        }

        final_list = self._get_data_list(
            sources,
            source_classes,
            code_link_template="https://zenless.hoyoverse.com/redemption?code={code}"
        )

        if final_list:
            logger.info(f"Total number of codes: {len(final_list)}")

        return final_list

    def get_sources(self, config_path: str) -> List[str]:
        source_key = "zzz_sources"

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
        return super()._get_data_list(sources, source_classes, code_link_template, game="zzz")
