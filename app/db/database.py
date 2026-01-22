import sqlite3


class Database:
    def __init__(self, db_path: str = "bot.db"):
        self.connection = sqlite3.connect(
            db_path,
            check_same_thread=False,
        )
        self.connection.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def close(self):
        self.connection.close()