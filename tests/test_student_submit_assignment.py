
from app.db.database import Database

from app.db.repositories.users import UserRepository
from app.db.repositories.groups import GroupRepository
from app.db.repositories.subjects import SubjectRepository
from app.db.repositories.assignments import AssignmentRepository
from app.db.repositories.submissions import SubmissionRepository

def test_student_submit_assignment():
    db = Database(":memory:")

    user_repo = UserRepository(db)
    group_repo = GroupRepository(db)
    subject_repo = SubjectRepository(db)
    assignment_repo = AssignmentRepository(db)
    submission_repo = SubmissionRepository(db)

    user_repo.create(1, role="teacher")
    user_repo.create(2, role="student")

    group_repo.create("ИТ-15")
    subject_repo.create("Программирование", teacher_id=1)

    group = group_repo.get_by_name("ИТ-15")
    subject = subject_repo.get_by_teacher(1)[0]

    assignment_repo.create(
        title="ДЗ №1",
        description="Решить задачи",
        subject_id=subject["id"],
        group_id=group["id"],
    )

    assignment = assignment_repo.get_by_group(group["id"])[0]

    submission_repo.create(
        assignment_id=assignment["id"],
        student_id=2,
        text="Моё решение",
    )

    subs = submission_repo.get_by_assignment(assignment["id"])

    assert len(subs) == 1
    assert subs[0]["text"] == "Моё решение"

    db.close()