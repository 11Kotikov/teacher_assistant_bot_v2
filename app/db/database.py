import sqlite3
from pathlib import Path

DB_PATH = Path("data")
DB_PATH.mkdir(exist_ok=True)

DATABASE_FILE = DB_PATH / "bot.db"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_FILE,
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def close(self):
        self.connection.close()
