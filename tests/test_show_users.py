from app.db.database import Database
from app.db.repositories.users import UserRepository

def test_show_users():
    db = Database(":memory:")
    repo = UserRepository(db)

    repo.create(1, role="student")
    repo.create(2, role="teacher")

    users = repo.get_all()

    assert len(users) == 2
    assert users[0]["telegram_id"] == 1
    assert users[1]["role"] == "teacher"

    db.close()