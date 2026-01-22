from app.db.database import Database
from app.db.repositories.submissions import SubmissionRepository


class SubmissionService:
    def __init__(self, db: Database):
        self.repo = SubmissionRepository(db)

    def submit_text(
        self,
        assignment_id: int,
        student_id: int,
        text: str,
    ):
        self.repo.create(
            assignment_id=assignment_id,
            student_id=student_id,
            text=text,
        )