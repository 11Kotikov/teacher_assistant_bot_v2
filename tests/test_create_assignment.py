from app.db.database import Database
from app.db.repositories.users import UserRepository
from app.db.repositories.groups import GroupRepository
from app.db.repositories.subjects import SubjectRepository
from app.db.repositories.assignments import AssignmentRepository

def test_create_assignment():
    db = Database(":memory:")

    user_repo = UserRepository(db)
    group_repo = GroupRepository(db)
    subject_repo = SubjectRepository(db)
    assignment_repo = AssignmentRepository(db)

    user_repo.create(1, role="teacher")
    group_repo.create("ИТ-15")
    subject_repo.create("Математика", teacher_id=1)

    group = group_repo.get_by_name("ИТ-15")
    subject = subject_repo.get_by_teacher(1)[0]

    assignment_repo.create(
        title="ДЗ №1",
        description="Решить задачи 1–5",
        subject_id=subject["id"],
        group_id=group["id"],
    )

    assignments = assignment_repo.get_by_group(group["id"])

    assert len(assignments) == 1
    assert assignments[0]["title"] == "ДЗ №1"

    db.close()