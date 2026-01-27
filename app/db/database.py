import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "bot.db"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row

        print("DB PATH:", DB_PATH)

    def execute(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_one(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.connection.close()
