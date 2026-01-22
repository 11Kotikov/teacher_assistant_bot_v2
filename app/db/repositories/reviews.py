from app.db.database import Database
from app.db.models import REVIEW_TABLE


class ReviewRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(REVIEW_TABLE)

    def create(
        self,
        submission_id: int,
        teacher_id: int,
        grade: int,
        comment: str,
    ):
        self.db.execute(
            """
            INSERT INTO reviews (submission_id, teacher_id, grade, comment)
            VALUES (?, ?, ?, ?)
            """,
            (submission_id, teacher_id, grade, comment),
        )

    def get_by_submission(self, submission_id: int):
        cur = self.db.execute(
            "SELECT * FROM reviews WHERE submission_id = ?",
            (submission_id,),
        )
        return cur.fetchone()