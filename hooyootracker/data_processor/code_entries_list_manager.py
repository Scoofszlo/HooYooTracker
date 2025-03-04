from typing import Dict, List
from hooyootracker.data_processor._exceptions import InvalidGameType
from hooyootracker.data_processor.model import (
    DataModel,
    GenshinImpactDM,
    ZenlessZoneZeroDM
)


class CodeEntriesListManager():
    def __init__(self, game: str, config_path: str) -> None:
        self.controller: DataModel = self._get_controller_class(game)
        self.sources: List[str] = self.controller.get_sources(config_path)
        self.entries_list: List[Dict[str, str]] = []

    def get_data(self) -> None:
        if not self.entries_list:
            self.entries_list = self.controller.get_data(self.sources)

        return self.entries_list

    def update_data(self) -> None:
        self.entries_list = self.controller.update_data(self.sources)

    @staticmethod
    def _get_controller_class(game: str) -> DataModel:
        try:
            CODE_ENTRIES_LIST_CONTROLLER = {
                "gi": GenshinImpactDM,
                "zzz": ZenlessZoneZeroDM
            }

            return CODE_ENTRIES_LIST_CONTROLLER[game](game)
        except (ValueError, KeyError):
            raise InvalidGameType(game) from None
