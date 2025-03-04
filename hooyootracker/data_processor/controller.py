import toml
from abc import abstractmethod
from typing import Any, Dict, List, Tuple
from hooyootracker.db.model import Database
from hooyootracker.data_processor._exceptions import FileParsingError
from hooyootracker.logger import Logger
from hooyootracker.scraper import gi, zzz
from hooyootracker.scraper.model import CodeEntriesList, Scraper

logger = Logger()


class CodeEntriesListController:
    def __init__(self, game: str):
        self.db: Database = Database()
        self.entries_list: List[Tuple[Any, ...]] = self._restructure_as_dict(self.db.get_data(game))
        self.config: Dict[str, Any] = None

    @abstractmethod
    def get_data(self, sources: List[str]) -> List[Dict[str, str]]:
        """
        Process data based from specified sources and returns it with a list
        of codes and its reward details
        """

    @abstractmethod
    def get_sources(self, config_path: str, source_key: str) -> Dict[str, Any]:
        """
        This method retrieves a list of source names from the config
        file, which then returns a list of strings containing source names.
        """

    @abstractmethod
    def _get_scraper_classes(self) -> Dict[str, Scraper]:
        pass

    def _get_config(self, config_path: str) -> Dict[str, Any]:
        """
        This parses the config file specified from the path and loads it.
        If there is an error parsing the config file, this will result in
        exception, thus halting the program.
        """

        if self.config is None:
            logger.debug(f"Attempting to open config file at: {config_path}")

            try:
                with open(config_path, 'r') as file:
                    self.config = toml.load(file)
                logger.debug("Config file loaded successfully")
            except Exception as e:
                logger.critical(f"Error parsing config file: {e}", exc_info=True)
                raise FileParsingError from e

        return self.config

    def _get_data_list(
            self,
            sources: List[str],
            source_classes: Dict[str, Scraper],
            code_link_template: str,
    ) -> List[Dict[str, str | List]] | None:
        """
        Processes all the data based on specified sources and returns the
        procesed data into a list of dictionaries containing the code,
        reward details, and source details.
        """
        if sources is None:
            logger.info("No list of sources have been passed. Nothing will be processed.")
            return None
        else:
            logger.info(f"Getting latest changes from {len(sources)} source{'s' if len(sources) > 1 else ''} ")

        entries_list = []

        for source in sources:
            if source in source_classes:
                entry = source_classes[source]().get_data()

                if entry is None:
                    continue

                entries_list.append(entry)
            else:
                logger.info(f"\"{source}\" does not exist in available scrapers. Skipping.")
        entries_list = self._remove_duplicate_entries(entries_list, code_link_template)

        return entries_list

    def _remove_duplicate_entries(
            self,
            code_entries_lists: List[CodeEntriesList],
            code_link_template: str,
    ) -> List[Dict[str, str]]:
        if code_entries_lists is None:
            return None

        clean_list = []

        if len(code_entries_lists) == 1:
            for source in code_entries_lists:
                if not source.code_list:
                    return None

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
            source: Dict[str, str | List],
            entry: Dict[str, str],
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
    ) -> List[Dict[str, str]]:
        # Return a list containing no values if there is nothing to process
        if not entries_list[0] and not entries_list[1]:
            return []

        data = {
            "metadata": {
                "metadata_id": entries_list[0][0][0],
                "game": entries_list[0][0][1],
                "modified_date": entries_list[0][0][2]
            },
            "entries_list": []
        }

        for entry in entries_list[1]:
            code_info = {
                "game": entry[2],
                "source_name": entry[6],
                "source_url": entry[7],
                "code": entry[3],
                "reward_details": entry[4],
                "code_link": entry[5]
            }

            data["entries_list"].append(code_info)

        return data


class GenshinImpactDM(CodeEntriesListController):
    def get_data(self, sources: List[str]) -> List[Tuple[Any, ...]]:
        if not self.entries_list:
            scraper_classes = self._get_scraper_classes()

            entries_list = self._get_data_list(
                sources,
                scraper_classes,
                code_link_template="https://genshin.hoyoverse.com/en/gift?code={code}",
            )

            self.db.insert_data(entries_list, "gi")
            self.entries_list = self.db.get_data("gi")
            self.entries_list = self._restructure_as_dict(self.entries_list)

            if self.entries_list:
                logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def get_sources(self, config_path: str) -> List[str]:
        config = self._get_config(config_path)
        source_key = "gi_sources"
        sources = config['sources'][source_key]
        logger.debug(f"Sources retrieved: {sources}")

        return sources

    def update_data(self, sources: List[str]):
        scraper_classes = self._get_scraper_classes()

        entries_list = self._get_data_list(
            sources,
            scraper_classes,
            code_link_template="https://genshin.hoyoverse.com/en/gift?code={code}",
        )

        self.db.insert_data(entries_list, "gi")
        self.entries_list = self.db.get_data("gi")
        self.entries_list = self._restructure_as_dict(self.entries_list)

        if self.entries_list:
            logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def _get_scraper_classes(self) -> Dict[str, Scraper]:
        scraper_classes = {
            "PocketTactics": gi.PocketTactics,
            "Game8": gi.Game8,
            "RockPaperShotgun": gi.RockPaperShotgun,
            "VG247": gi.VG247
        }

        return scraper_classes


class ZenlessZoneZeroDM(CodeEntriesListController):
    def get_data(self, sources: List[str]) -> List[Dict[str, str]]:
        if not self.entries_list:
            scraper_classes = self._get_scraper_classes()

            entries_list = self._get_data_list(
                sources,
                scraper_classes,
                code_link_template="https://zenless.hoyoverse.com/redemption?code={code}",
            )

            self.db.insert_data(entries_list, "zzz")
            self.entries_list = self.db.get_data("zzz")
            self.entries_list = self._restructure_as_dict(self.entries_list)

            if self.entries_list:
                logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def get_sources(self, config_path: str) -> List[str]:
        config = self._get_config(config_path)
        source_key = "zzz_sources"
        sources = config['sources'][source_key]
        logger.debug(f"Sources retrieved: {sources}")

        return sources

    def update_data(self, sources: List[str]) -> List[Tuple[Any, ...]]:
        scraper_classes = self._get_scraper_classes()

        entries_list = self._get_data_list(
            sources,
            scraper_classes,
            code_link_template="https://zenless.hoyoverse.com/redemption?code={code}",
        )

        self.db.insert_data(entries_list, "zzz")
        self.entries_list = self.db.get_data("zzz")
        self.entries_list = self._restructure_as_dict(self.entries_list)

        if self.entries_list:
            logger.info(f"Total number of codes: {len(self.entries_list['entries_list'])}")

        return self.entries_list

    def _get_scraper_classes(self) -> Dict[str, Scraper]:
        scraper_classes = {
            "PocketTactics": zzz.PocketTactics,
            "Game8": zzz.Game8,
            "Polygon": zzz.Polygon,
            "VG247": zzz.VG247
        }

        return scraper_classes
