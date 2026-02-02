from app.db.database import Database
from app.db.repositories.users import UserRepository

db = Database()
repo = UserRepository(db)

repo.set_group(telegram_id=205411683, group_id=2)

db.close()