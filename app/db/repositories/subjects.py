from app.db.database import Database
from app.db.models import SUBJECT_TABLE


class SubjectRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(SUBJECT_TABLE)

    def create(self, name: str, teacher_id: int):
        self.db.execute(
            "INSERT INTO subjects (name, teacher_id) VALUES (?, ?)",
            (name, teacher_id),
        )

    def get_by_teacher(self, teacher_id: int):
        cur = self.db.execute(
            "SELECT * FROM subjects WHERE teacher_id = ?",
            (teacher_id,),
        )
        return cur.fetchall()