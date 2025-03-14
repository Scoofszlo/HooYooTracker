from typing import Dict, Union
from hooyootracker.codeentrieslist.controller import CodeEntriesListController, _get_controller_class


class CodeEntriesListManager():
    def __init__(self, game: str) -> None:
        self.controller: CodeEntriesListController = _get_controller_class(game)
        self.entries_list: Dict[str, Union[dict, list]] = {}

    def get_data(self) -> Dict[str, Union[dict, list]]:
        if not self.entries_list:
            self.entries_list = self.controller.get_data()

        return self.entries_list

    def update_data(self):
        self.entries_list = self.controller.update_data()
