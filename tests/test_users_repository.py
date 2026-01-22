from app.db.database import Database
from app.db.repositories.users import UserRepository


def test_create_and_get_user():
    db = Database()
    repo = UserRepository(db)

    telegram_id = 123456789
    repo.create(telegram_id, role="student")

    user = repo.get_by_telegram_id(telegram_id)

    assert user is not None
    assert user["telegram_id"] == telegram_id
    assert user["role"] == "student"

    db.close()
