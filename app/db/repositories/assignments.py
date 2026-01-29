from app.db.database import Database
from app.db.models import ASSIGNMENT_TABLE


class AssignmentRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(ASSIGNMENT_TABLE)
        self._ensure_deadline_column()

    def _ensure_deadline_column(self):
        columns = self.db.fetch_all("PRAGMA table_info(assignments)")
        column_names = {column["name"] for column in columns}
        if "deadline" not in column_names:
            self.db.execute("ALTER TABLE assignments ADD COLUMN deadline TIMESTAMP")

    def create(
        self,
        title: str,
        description: str,
        deadline: str | None,
        subject_id: int,
        group_id: int,
    ):
        self.db.execute(
            """
            INSERT INTO assignments (title, description, deadline, subject_id, group_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, description, deadline, subject_id, group_id),
        )

    def get_by_group(self, group_id: int):
        cur = self.db.execute(
            "SELECT * FROM assignments WHERE group_id = ?",
            (group_id,),
        )
        return cur.fetchall()
    
    def get_all(self):
        return self.db.fetch_all("SELECT * FROM assignments")
    
    def get_by_group(self, group_id: int):
        return self.db.fetch_all(
            "SELECT * FROM assignments WHERE group_id = ?",
            (group_id,)
        )