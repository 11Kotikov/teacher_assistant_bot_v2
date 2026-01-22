from app.db.database import Database
from app.db.repositories.reviews import ReviewRepository
from app.db.repositories.submissions import SubmissionRepository


def test_teacher_review_submission():
    db = Database(":memory:")

    review_repo = ReviewRepository(db)
    submission_repo = SubmissionRepository(db)

    submission_repo.create(
        assignment_id=1,
        student_id=2,
        text="Моё решение",
    )

    review_repo.create(
        submission_id=1,
        teacher_id=1,
        grade=5,
        comment="Хорошая работа",
    )

    review = review_repo.get_by_submission(1)

    assert review["grade"] == 5
    assert review["comment"] == "Хорошая работа"

    db.close()
