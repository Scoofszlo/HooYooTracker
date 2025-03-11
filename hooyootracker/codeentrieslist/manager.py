from typing import Dict, Union
from hooyootracker.constants import Game
from hooyootracker.codeentrieslist._exceptions import InvalidGameType
from hooyootracker.codeentrieslist.controller import (
    CodeEntriesListController,
    GenshinImpactCELC,
    ZenlessZoneZeroCELC
)


class CodeEntriesListManager():
    def __init__(self, game: str, config_path: str) -> None:
        self.controller: CodeEntriesListController = self._get_controller_class(game, config_path)
        self.entries_list: Dict[str, Union[dict, list]] = {}

    def get_data(self) -> Dict[str, Union[dict, list]]:
        if not self.entries_list:
            self.entries_list = self.controller.get_data()

        return self.entries_list

    def update_data(self):
        self.entries_list = self.controller.update_data()

    @staticmethod
    def _get_controller_class(game: str, config_path: str) -> CodeEntriesListController:
        try:
            CODE_ENTRIES_LIST_CONTROLLER = {
                Game.GENSHIN_IMPACT.value: GenshinImpactCELC,
                Game.ZENLESS_ZONE_ZERO.value: ZenlessZoneZeroCELC
            }

            return CODE_ENTRIES_LIST_CONTROLLER[game](game, config_path)
        except (ValueError, KeyError):
            raise InvalidGameType(game) from None
