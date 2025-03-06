from typing import Dict, List
from hooyootracker.data_processor._exceptions import InvalidGameType
from hooyootracker.data_processor.controller import (
    CodeEntriesListController,
    GenshinImpactCELC,
    ZenlessZoneZeroCELC
)


class CodeEntriesListManager():
    def __init__(self, game: str, config_path: str) -> None:
        self.controller: CodeEntriesListController = self._get_controller_class(game, config_path)
        self.sources: List[str] = self.controller.get_sources(config_path)
        self.entries_list: List[Dict[str, str]] = []

    def get_data(self) -> None:
        if not self.entries_list:
            self.entries_list = self.controller.get_data(self.sources)

        return self.entries_list

    def update_data(self) -> None:
        self.entries_list = self.controller.update_data(self.sources)

    @staticmethod
    def _get_controller_class(game: str, config_path: str) -> CodeEntriesListController:
        try:
            CODE_ENTRIES_LIST_CONTROLLER = {
                "gi": GenshinImpactCELC,
                "zzz": ZenlessZoneZeroCELC
            }

            return CODE_ENTRIES_LIST_CONTROLLER[game](game, config_path)
        except (ValueError, KeyError):
            raise InvalidGameType(game) from None
