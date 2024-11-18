import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Any
from hooyootracker.constants import DB_FILE_PATH
from hooyootracker.logger import Logger

logger = Logger()


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILE_PATH)
        self.cursor = self.connection.cursor()
        self._init_tables()

    def insert_data(self, code_list: List[Dict[str, str]], game: str):
        # Initialize variables
        metadata_id = self._set_metadata_id(game)
        modified_date = self._get_date_now()

        # Insert or update metadata details
        if not self._check_metadata_details_exist(metadata_id):
            self._insert_metadata_details(metadata_id, game, modified_date)
        else:
            self._update_metadata_details(metadata_id, game, modified_date)

        # This inserts new data if there are no entries existing in the
        # database. Otherwise, it will remove all the entries associated
        # and insert the new data
        if self._check_code_entries_exists(game):
            self._delete_records(game)

        for entry in code_list:
            self._insert_entry(entry, metadata_id)

    def get_data(self, table: str, game: str) -> List[Tuple[Any, ...]]:
        query = f"SELECT * FROM {table} WHERE game = ?;"

        self.cursor.execute(query, (game,))
        data = self.cursor.fetchall()

        return data

    def _insert_metadata_details(
            self,
            metadata_id: int,
            game: str,
            modified_date: str
    ) -> None:
        logger.info(f"No metadata details associated with 'metadata_id = {metadata_id}' found. Inserting data...")

        query = """
                INSERT INTO metadata (metadata_id, game, modified_date)
                VALUES (?, ?, ?);
                """
        self.cursor.execute(query, (metadata_id, game, modified_date,))
        self.connection.commit()

        logger.info(f"Metadata details inserted successfully. (metadata_id: {metadata_id}, game: {game}, modified_date: {modified_date})")

    def _init_tables(self) -> None:
        if not self._check_table_exists(table_name="metadata"):
            query = """
                    CREATE TABLE metadata (
                        metadata_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        game TEXT,
                        modified_date TEXT
                    );
                    """
            self.cursor.execute(query)
            self.connection.commit()

            logger.info(f"Creating database table 'metadata' success. (query: {query})")
        else:
            logger.info("Table 'metadata' already exist. Skipping")

        if not self._check_table_exists(table_name="code_entries"):
            query = """
                    CREATE TABLE code_entries (
                        metadata_id INTEGER NOT NULL,
                        code_entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        game INTEGER NOT NULL,
                        code TEXT NOT NULL,
                        reward_details TEXT NOT NULL,
                        source_name TEXT NOT NULL,
                        source_url TEXT NOT NULL,
                        FOREIGN KEY (metadata_id) REFERENCES metadata(metadata_id)
                    );
                    """
            self.cursor.execute(query)
            self.connection.commit()

            logger.info(f"Creating database table 'code_entries' success. (query: {query})")
        else:
            logger.info("Table 'code_entries' already exist. Skipping")

    def _update_metadata_details(
            self,
            metadata_id: int,
            game: str,
            modified_date: str
    ) -> None:
        logger.info(f"Existing metadetails found associated with {metadata_id}. Updating data...")

        query = """
                UPDATE metadata SET modified_date = ? WHERE game = ?;
                """
        self.cursor.execute(query, (modified_date, game,))
        self.connection.commit()

        logger.info(f"Metadata details updated successfully. (metadata_id: {metadata_id}, game: {game}, modified_date: {modified_date})")

    def _insert_entry(self, entry: Dict[str, str], metadata_id: int) -> None:
        logger.debug(f"Inserting entry: {entry}")

        game = entry['game']
        code = entry['code']
        reward_details = entry['reward_desc']
        source_name = entry['source_name']
        source_url = entry['source_url']

        query = """
                INSERT INTO code_entries (metadata_id, game, code, reward_details, source_name, source_url)
                VALUES (?, ?, ?, ?, ?, ?);
                """
        self.cursor.execute(query, (metadata_id, game, code, reward_details, source_name, source_url))
        self.connection.commit()

    def _delete_records(self, game: str) -> None:
        logger.info(f"Deleting all records associated with 'game = {game}'")

        query = """
                DELETE from code_entries WHERE game = ?;
                """
        self.cursor.execute(query, (game,))

        self.connection.commit()
        logger.info("Deleting code entries successfully")

    def _check_table_exists(self, table_name: str) -> None:
        query = """
                SELECT name FROM sqlite_master WHERE type='table' AND name=?;
                """

        self.cursor.execute(query, (table_name,))

        return self.cursor.fetchone() is not None

    def _check_metadata_details_exist(self, metadata_id: int) -> bool:
        query = """
                SELECT 1 FROM metadata WHERE metadata_id = ?;
                """

        self.cursor.execute(query, (metadata_id,))

        return self.cursor.fetchone() is not None

    def _check_code_entries_exists(self, game: str):
        query = """
                SELECT 1 FROM code_entries WHERE game = ?;
                """

        self.cursor.execute(query, (game,))

        return self.cursor.fetchone() is not None

    def _get_date_now(self) -> str:
        return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")

    def _set_metadata_id(self, game: str) -> int:
        if game == "gi":
            metadata_id = 1
        elif game == "zzz":
            metadata_id = 2

        return metadata_id
