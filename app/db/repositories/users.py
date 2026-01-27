from app.db.database import Database
from app.db.models import USER_TABLE


class UserRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(USER_TABLE)

    def get_by_telegram_id(self, telegram_id: int):
        cursor = self.db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        return cursor.fetchone()

    def create(self, telegram_id: int, role: str | None = None):
        self.db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, role) VALUES (?, ?)",
            (telegram_id, role)
        )

    def set_group(self, telegram_id: int, group_id: int):
        self.db.execute(
            "UPDATE users SET group_id = ? WHERE telegram_id = ?",
            (group_id, telegram_id),
        )
        
    def get_students_by_group(self, group_id: int):
        return self.db.fetch_all(
            """
            SELECT telegram_id, first_name, last_name
            FROM users
            WHERE role = 'student' AND group_id = ?
            """,
            (group_id,),
        )

    def get_students_without_group(self):
        return self.db.fetch_all(
            """
            SELECT telegram_id, first_name, last_name
            FROM users
            WHERE role = 'student' AND group_id IS NULL
            """
        )

          
    def get_all(self):
        cur = self.db.execute("SELECT * FROM users")
        return cur.fetchall()