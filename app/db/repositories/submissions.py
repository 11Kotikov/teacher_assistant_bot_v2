from app.db.database import Database
from app.db.models import SUBMISSION_TABLE


class SubmissionRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(SUBMISSION_TABLE)

    def create(
        self,
        assignment_id: int,
        student_id: int,
        text: str | None = None,
        file_path: str | None = None,
    ):
        self.db.execute(
            """
            INSERT INTO submissions (assignment_id, student_id, text, file_path)
            VALUES (?, ?, ?, ?)
            """,
            (assignment_id, student_id, text, file_path),
        )

    def get_by_assignment(self, assignment_id: int):
        cur = self.db.execute(
        """
        SELECT *
        FROM submissions
        WHERE assignment_id = ?
        ORDER BY created_at ASC
        """,
        (assignment_id,)
        )
        return cur.fetchall()
    
    def exists(self, assignment_id: int, student_id: int) -> bool:
        result = self.db.fetch_one(
            "SELECT * FROM submissions WHERE assignment_id = ? AND student_id = ?",
            (assignment_id, student_id)
        )
        return result is not None
