import toml
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from hooyootracker.logging.logger import logger
from hooyootracker.constants import Game, Source
from hooyootracker.db.database import Database
from hooyootracker.codeentrieslist._exceptions import FileParsingError
from hooyootracker.scraper import gi, zzz
from hooyootracker.scraper.scraper import CodeEntriesList, CodeEntry, Scraper


class CodeEntriesListController:
    def __init__(self, game: str, config_path: str):
        self.db: Database = Database()
        self.config: Dict[str, Any] = self._get_config(config_path)
        self.source_key: str
        self.scraper_classes: Dict[str, type[Scraper]]
        self.scrapers: List[type[Scraper]] = self.get_scrapers(
            source_key=self.source_key,
            scraper_classes=self.scraper_classes
        )
        self.entries_list: Dict[str, Union[dict, list]] = self._restructure_as_dict(self.db.get_data(game))

    @abstractmethod
    def get_data(self) -> Dict[str, Union[dict, list]]:
        """
        Process data based from specified sources and returns it with a list
        of codes and its reward details
        """

    @abstractmethod
    def update_data(self):
        """
        Updates the data by deleting all the records from the database,
        retrieving the latest data from specified sources, and returning it
        with a list of codes and its reward details
        """

    def get_scrapers(self, source_key: str, scraper_classes: Dict[str, type[Scraper]]) -> List[type[Scraper]]:
        """
        This gets the list of scrapers to be used based on the sources listed
        from the config file
        """
        sources = self.config['sources'][source_key]

        scraper_list: List[type[Scraper]] = []

        for source in sources:
            if source in scraper_classes:
                scraper_list.append(scraper_classes[source])
            else:
                logger.info(f"\"{source}\" does not exist in available scrapers. Skipping.")

        return scraper_list

    def _get_config(self, config_path: str):
        """
        This parses the config file specified from the path and loads it.
        If there is an error parsing the config file, this will result in
        exception, thus halting the program.
        """

        logger.debug(f"Attempting to open config file at: {config_path}")

        try:
            with open(config_path, 'r') as file:
                return toml.load(file)
            logger.debug("Config file loaded successfully")
        except Exception as e:
            logger.critical(f"Error parsing config file: {e}", exc_info=True)
            raise FileParsingError from e

    def _get_data_list(self, code_link_template: str) -> List[Dict[str, str]]:
        """
        Processes all the data based on specified sources and returns the
        procesed data into a list of dictionaries containing the code,
        reward details, and source details.
        """
        if not self.scrapers:
            logger.info("No list of scrapers are available. Nothing will be processed.")
            return []
        else:
            logger.info(f"Getting latest changes from {len(self.scrapers)} source{'s' if len(self.scrapers) > 1 else ''} ")

        entries_list: List[CodeEntriesList] = []

        for scraper in self.scrapers:
            entry = scraper().get_data()

            if entry is None:
                continue

            entries_list.append(entry)
        clean_list = self._remove_duplicate_entries(entries_list, code_link_template)

        return clean_list

    def _remove_duplicate_entries(
            self,
            code_entries_lists: List[CodeEntriesList],
            code_link_template: str,
    ) -> List[Dict[str, str]]:
        if not code_entries_lists:
            return []

        clean_list = []

        if len(code_entries_lists) == 1:
            for source in code_entries_lists:
                if not source.code_list:
                    return []

                for entry in source.code_list:
                    code = entry.code

                    code_info = self._get_code_info(source, entry, code_link_template, code)

                    clean_list.append(code_info)

        elif len(code_entries_lists) >= 2:
            unique_list = set()
            total_duplicate_codes = 0

            logger.info(f"Removing potential duplicate code entries from {len(code_entries_lists)} sources")

            for source in code_entries_lists:
                logger.debug(f"Processing source: {source.source_name}")

                if not source.code_list:
                    continue

                for entry in source.code_list:
                    code = entry.code

                    if code not in unique_list:
                        unique_list.add(code)

                        code_info = self._get_code_info(source, entry, code_link_template, code)

                        clean_list.append(code_info)
                        logger.debug(f"Skipping {code} ({source.source_name}) as it is unique")
                    else:
                        total_duplicate_codes += 1
                        logger.debug(f"Duplicate code found: {code} ({source.source_name})")

            logger.debug(f"Removed {total_duplicate_codes} duplicate codes")

        return clean_list

    def _get_code_info(
            self,
            source: CodeEntriesList,
            entry: CodeEntry,
            code_link_template: str,
            code: str,
    ) -> Dict[str, str]:

        code_info = {
            "code": code,
            "reward_details": entry.reward_details,
            "code_link": code_link_template.format(code=code),
            "source_name": source.source_name,
            "source_url": source.source_url,
        }

        return code_info

    def _restructure_as_dict(
            self,
            entries_list: List[Tuple[Any, ...]]
    ) -> Dict[str, Union[dict, List[dict]]]:
        # Return a list containing no values if there is nothing to process
        if not entries_list:
            return {}

        data: Dict[str, Union[dict, List[dict]]] = {
            "metadata": {
                "metadata_id": entries_list[0][0],
                "game": entries_list[0][1],
                "modified_date": entries_list[0][2]
            },
            "entries_list": []
        }

        for entry in entries_list:
            code_info: dict = {
                "game": entry[1],
                "source_name": entry[3],
                "source_url": entry[4],
                "code": entry[5],
                "reward_details": entry[6],
                "code_link": entry[7]
            }

            if isinstance(data["entries_list"], list):
                data["entries_list"].append(code_info)

        return data


class GenshinImpactCELC(CodeEntriesListController):
    def __init__(self, game: str, config_path: str):
        self.source_key = "zzz_sources"
        self.scraper_classes = {
            Source.POCKET_TACTICS.value: gi.PocketTactics,
            Source.GAME8.value: gi.Game8,
            Source.ROCK_PAPER_SHOTGUN.value: gi.RockPaperShotgun,
            Source.VG247.value: gi.VG247
        }
        super().__init__(game, config_path)

    def get_data(self) -> Dict[str, Union[dict, list]]:
        if not self.entries_list:
            entries_list = self._get_data_list(
                code_link_template="https://genshin.hoyoverse.com/en/gift?code={code}",
            )

            self.db.insert_data(entries_list, Game.GENSHIN_IMPACT.value)
            raw_entries_list = self.db.get_data(Game.GENSHIN_IMPACT.value)
            self.entries_list = self._restructure_as_dict(raw_entries_list)

            if self.entries_list:
                logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def update_data(self) -> Dict[str, Union[dict, list]]:
        entries_list = self._get_data_list(
            code_link_template="https://genshin.hoyoverse.com/en/gift?code={code}",
        )

        self.db.insert_data(entries_list, Game.GENSHIN_IMPACT.value)
        raw_entries_list = self.db.get_data(Game.GENSHIN_IMPACT.value)
        self.entries_list = self._restructure_as_dict(raw_entries_list)

        if self.entries_list:
            logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list


class ZenlessZoneZeroCELC(CodeEntriesListController):
    def __init__(self, game: str, config_path: str):
        self.source_key = "zzz_sources"
        self.scraper_classes = {
            Source.POCKET_TACTICS.value: zzz.PocketTactics,
            Source.GAME8.value: zzz.Game8,
            Source.POLYGON.value: zzz.Polygon,
            Source.VG247.value: zzz.VG247
        }
        super().__init__(game, config_path)

    def get_data(self) -> Dict[str, Union[dict, list]]:
        if not self.entries_list:
            entries_list = self._get_data_list(
                code_link_template="https://zenless.hoyoverse.com/redemption?code={code}",
            )

            self.db.insert_data(entries_list, Game.ZENLESS_ZONE_ZERO.value)
            raw_entries_list = self.db.get_data(Game.ZENLESS_ZONE_ZERO.value)
            self.entries_list = self._restructure_as_dict(raw_entries_list)

            if self.entries_list:
                logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def update_data(self) -> Dict[str, Union[dict, list]]:
        entries_list = self._get_data_list(
            code_link_template="https://zenless.hoyoverse.com/redemption?code={code}",
        )

        self.db.insert_data(entries_list, Game.ZENLESS_ZONE_ZERO.value)
        raw_entries_list = self.db.get_data(Game.ZENLESS_ZONE_ZERO.value)
        self.entries_list = self._restructure_as_dict(raw_entries_list)

        if self.entries_list:
            logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list
