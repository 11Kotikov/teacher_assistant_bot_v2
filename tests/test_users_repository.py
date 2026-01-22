from app.db.database import Database
from app.db.repositories.groups import GroupRepository
from app.db.repositories.users import UserRepository


def test_create_and_get_user():
    db = Database(":memory:")
    repo = UserRepository(db)

    telegram_id = 123456789
    repo.create(telegram_id, role="student")

    user = repo.get_by_telegram_id(telegram_id)

    assert user is not None
    assert user["telegram_id"] == telegram_id
    assert user["role"] == "student"

    db.close()
    

def test_create_and_get_groups():
    db = Database(":memory:")
    repo = GroupRepository(db)

    repo.create("ИТ-15")
    repo.create("ИС-25")

    groups = repo.get_all()

    names = [g["name"] for g in groups]

    assert "ИТ-15" in names
    assert "ИС-25" in names

    db.close()  
    
def test_set_group_for_user():
    db = Database(":memory:")
    user_repo = UserRepository(db)
    group_repo = GroupRepository(db)

    user_repo.create(111, role="student")
    group_repo.create("ИТ-15")

    group = group_repo.get_by_name("ИТ-15")
    user_repo.set_group(111, group["id"])

    user = user_repo.get_by_telegram_id(111)

    assert user["group_id"] == group["id"]

    db.close()
