from app.db.database import Database
from app.db.repositories.users import UserRepository

def test_show_users():
    db = Database()
    repo = UserRepository(db)

    users = db.execute("SELECT * FROM users").fetchall()
    print(users)

    db.close()