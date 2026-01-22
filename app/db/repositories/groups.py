from app.db.database import Database
from app.db.models import GROUP_TABLE


class GroupRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(GROUP_TABLE)

    def create(self, name: str):
        self.db.execute(
            "INSERT OR IGNORE INTO groups (name) VALUES (?)",
            (name,)
        )

    def get_all(self):
        cursor = self.db.execute(
            "SELECT * FROM groups ORDER BY name"
        )
        return cursor.fetchall()

    def get_by_name(self, name: str):
        cursor = self.db.execute(
            "SELECT * FROM groups WHERE name = ?",
            (name,)
        )
        return cursor.fetchone()
