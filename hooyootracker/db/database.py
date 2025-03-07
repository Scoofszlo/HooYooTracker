import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Any
from hooyootracker.constants import DB_FILE_PATH, Game
from hooyootracker.logger import Logger

logger = Logger()


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILE_PATH, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._init_tables()

    def insert_data(self, code_list: List[Dict[str, str]], game: str):
        # Initialize variables
        game_id = self._get_game_id(game)
        modified_date = self._get_date_now()
        metadata_id: int

        # Insert or update metadata details
        if not self._check_metadata_details_exist(game_id):
            metadata_id = self._insert_metadata_details(game_id, modified_date)
        else:
            metadata_id = self._update_metadata_details(game_id, modified_date)

        # This inserts new data if there are no entries existing in the
        # database. Otherwise, it will remove all the entries associated
        # and insert the new data
        if self._check_code_entries_exists(game_id):
            self._delete_records(game_id)

        for entry in code_list:
            source_id = self._handle_source_data(entry)
            self._insert_entry(entry, metadata_id, game_id, source_id)

    def get_data(self, game: str) -> List[Tuple[Any, ...]]:
        query = """
                SELECT m.metadata_id, g.name, m.modified_date, g.name, src.name, src.url, ce.code, ce.reward_details, ce.reward_details, ce.code_link from code_entries as ce
                    INNER JOIN metadata as m ON g.game_id = m.game_id
                    INNER JOIN game as g ON g.name = ?
                    INNER JOIN sources as src ON src.source_id = ce.source_id
                    WHERE g.game_id = ce.game_id
                    ORDER BY ce.code_entry_id;
                """
        
        query2 = """
                SELECT m.metadata_id, g.name, m.modified_date, src.name, src.url, ce.code, ce.reward_details, ce.code_link 
                FROM code_entries AS ce
                INNER JOIN metadata AS m ON ce.game_id = m.game_id
                INNER JOIN game AS g ON g.game_id = ce.game_id
                INNER JOIN sources AS src ON src.source_id = ce.source_id
                WHERE g.name = ?
                ORDER BY ce.code_entry_id;
                """

        self.cursor.execute(query2, (game,))
        data = self.cursor.fetchall()

        return data

    def _insert_metadata_details(
            self,
            game_id: int,
            modified_date: str
    ) -> int:
        logger.info(f"No metadata details associated with 'game_id = {game_id}' found. Inserting data...")

        query = """
                INSERT INTO metadata (game_id, modified_date)
                VALUES (?, ?);
                """
        self.cursor.execute(query, (game_id, modified_date,))
        self.connection.commit()

        metadata_id = self.cursor.lastrowid

        logger.debug(f"Metadata details inserted successfully. (metadata_id: {metadata_id}, game: {game_id}, modified_date: {modified_date})")

        return metadata_id

    def _init_tables(self) -> None:
        if not self._check_table_exists(table_name="game"):
            create_table_query = """
                    CREATE TABLE game (
                        game_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT
                    );
                    """
            self.cursor.execute(create_table_query)
            self.connection.commit()

            logger.debug("Creating database table 'game' success.")

            data = [
                (1, Game.GENSHIN_IMPACT.value),
                (2, Game.ZENLESS_ZONE_ZERO.value)
            ]

            for datum in data:
                insert_data_query = """
                                    INSERT INTO game (game_id, name)
                                    VALUES (?, ?);
                                    """
                self.cursor.execute(insert_data_query, (datum[0], datum[1]))
                self.connection.commit()

        if not self._check_table_exists(table_name="sources"):
            query = """
                    CREATE TABLE sources (
                        source_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT,
                        url TEXT
                    );
                    """
            self.cursor.execute(query)
            self.connection.commit()

            logger.debug("Creating database table 'sources' success.")

        if not self._check_table_exists(table_name="metadata"):
            query = """
                    CREATE TABLE metadata (
                        metadata_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        game_id INTEGER NOT NULL,
                        modified_date TEXT NOT NULL,
                        FOREIGN KEY (game_id) REFERENCES game(game_id)
                    );
                    """
            self.cursor.execute(query)
            self.connection.commit()

            logger.debug("Creating database table 'metadata' success.")

        if not self._check_table_exists(table_name="code_entries"):
            query = """
                    CREATE TABLE code_entries (
                        code_entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        metadata_id INTEGER NOT NULL,
                        game_id INTEGER NOT NULL,
                        source_id INTEGER,
                        code TEXT NOT NULL,
                        reward_details TEXT NOT NULL,
                        code_link TEXT NOT NULL,
                        FOREIGN KEY (metadata_id) REFERENCES metadata(metadata_id),
                        FOREIGN KEY (game_id) REFERENCES metadata(game_id),
                        FOREIGN KEY (source_id) REFERENCES sources(source_id)
                    );
                    """
            self.cursor.execute(query)
            self.connection.commit()

            logger.debug("Creating database table 'code_entries' success.")

    def _update_metadata_details(
            self,
            game_id: int,
            modified_date: str
    ) -> None:
        logger.debug(f"Existing metadetails found associated with 'game_id = {game_id}'. Updating data...")

        query = """
                UPDATE metadata SET modified_date = ? WHERE game_id = ?;
                """
        self.cursor.execute(query, (modified_date, game_id,))
        self.connection.commit()

        metadata_id = self.cursor.lastrowid

        logger.debug(f"Metadata details updated successfully. (metadata_id: {metadata_id}, game: {game_id}, modified_date: {modified_date})")

        return metadata_id

    def _insert_entry(self, entry: Dict[str, str], metadata_id: int, game_id: int, source_id: int) -> None:
        logger.debug(f"Inserting entry: {entry}")

        code = entry['code']
        reward_details = entry['reward_details']
        code_link = entry['code_link']

        query = """
                INSERT INTO code_entries (metadata_id, game_id, source_id, code, reward_details, code_link)
                VALUES (?, ?, ?, ?, ?, ?);
                """
        self.cursor.execute(query, (metadata_id, game_id, source_id, code, reward_details, code_link,))
        self.connection.commit()

    def _delete_records(self, game_id: int) -> None:
        logger.debug(f"Deleting all records associated with 'game_id = {game_id}'")

        query = """
                DELETE from code_entries WHERE game_id = ?;
                """
        self.cursor.execute(query, (game_id,))

        self.connection.commit()
        logger.debug("Deleting code entries successfully")

    def _check_table_exists(self, table_name: str) -> None:
        query = """
                SELECT name FROM sqlite_master WHERE type='table' AND name=?;
                """

        self.cursor.execute(query, (table_name,))

        return self.cursor.fetchone() is not None

    def _check_metadata_details_exist(self, metadata_id: int) -> bool:
        query = """
                SELECT 1 FROM metadata WHERE game_id = ?;
                """

        self.cursor.execute(query, (metadata_id,))

        return self.cursor.fetchone() is not None

    def _check_code_entries_exists(self, game_id: int):
        query = """
                SELECT 1 FROM code_entries WHERE game_id = ?;
                """

        self.cursor.execute(query, (game_id,))

        return self.cursor.fetchone() is not None

    def _check_source_exists(self, source_name):
        query = """
                SELECT 1 FROM sources WHERE name = ?;
                """

        self.cursor.execute(query, (source_name,))

        return self.cursor.fetchone() is not None

    def _get_date_now(self) -> str:
        return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")

    def _set_metadata_id(self, game: str) -> int:
        if game == Game.GENSHIN_IMPACT.value:
            metadata_id = 1
        elif game == Game.ZENLESS_ZONE_ZERO.value:
            metadata_id = 2

        return metadata_id

    def _get_game_id(self, game: str) -> int:
        if game == Game.GENSHIN_IMPACT.value:
            metadata_id = 1
        elif game == Game.ZENLESS_ZONE_ZERO.value:
            metadata_id = 2

        return metadata_id

    def _handle_source_data(self, entry: Dict[str, str]) -> int:
        source_name = entry['source_name']
        source_url = entry['source_url']

        logger.debug(f"Handling source data for source_name: {source_name}, source_url: {source_url}")

        if not self._check_source_exists(source_name):
            logger.debug(f"Source '{source_name}' not found. Inserting new source.")
            query = """
                    INSERT INTO sources (name, url)
                    VALUES (?, ?);
                    """
            self.cursor.execute(query, (source_name, source_url,))
            self.connection.commit()

            source_id = self.cursor.lastrowid
            logger.debug(f"Source inserted successfully. (source_id: {source_id}, name: {source_name}, url: {source_url})")
            return source_id

        query = """
                SELECT source_id FROM sources WHERE name = ?;
                """
        self.cursor.execute(query, (source_name,))
        source_id = self.cursor.fetchone()[0]
        logger.debug(f"Source found. (source_id: {source_id}, name: {source_name})")
        return source_id
