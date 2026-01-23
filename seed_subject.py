from app.db.database import Database
from app.db.repositories.subjects import SubjectRepository


TEACHER_ID = 205411683  # <-- ВСТАВЬ СВОЙ TG ID

db = Database()
repo = SubjectRepository(db)

repo.create("Программирование", teacher_id=TEACHER_ID)

print("Предмет 'Программирование' добавлен")

db.close()