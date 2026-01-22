from app.db.database import Database
from app.db.models import ASSIGNMENT_TABLE


class AssignmentRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(ASSIGNMENT_TABLE)

    def create(
        self,
        title: str,
        description: str,
        subject_id: int,
        group_id: int,
    ):
        self.db.execute(
            """
            INSERT INTO assignments (title, description, subject_id, group_id)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, subject_id, group_id),
        )

    def get_by_group(self, group_id: int):
        cur = self.db.execute(
            "SELECT * FROM assignments WHERE group_id = ?",
            (group_id,),
        )
        return cur.fetchall()
