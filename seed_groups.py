from app.db.database import Database
from app.db.repositories.groups import GroupRepository

db = Database()
repo = GroupRepository(db)

repo.create("ИТ-15")
repo.create("ИТ-25")

print("Группы добавлены")

db.close()