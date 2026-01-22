from app.db.database import Database
from app.db.repositories.assignments import AssignmentRepository
from app.db.repositories.subjects import SubjectRepository


class AssignmentService:
    def __init__(self, db: Database):
        self.assignments = AssignmentRepository(db)
        self.subjects = SubjectRepository(db)

    def create_assignment(
        self,
        teacher_id: int,
        subject_name: str,
        title: str,
        description: str,
        group_id: int,
    ):
        subjects = self.subjects.get_by_teacher(teacher_id)
        subject = next((s for s in subjects if s["name"] == subject_name), None)
        if not subject:
            raise ValueError("Subject not found")

        self.assignments.create(
            title=title,
            description=description,
            subject_id=subject["id"],
            group_id=group_id,
        )
