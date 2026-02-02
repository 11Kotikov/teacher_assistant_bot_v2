from app.db.database import Database
from app.db.repositories.users import UserRepository

db = Database()
repo = UserRepository(db)

repo.set_role(205411683, "teacher")

db.close()
print("OK")
