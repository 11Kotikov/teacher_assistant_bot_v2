from app.db.database import Database
from app.db.repositories.subjects import SubjectRepository


TEACHER_TELEGRAM_ID = 205411683

BASE_SUBJECTS = [
    "Программирование",
    "Английский язык",
    "Обществознание",
]


def main():
    db = Database()
    repo = SubjectRepository(db)

    existing = repo.get_by_teacher(TEACHER_TELEGRAM_ID)
    existing_names = {s["name"] for s in existing}

    created = 0

    for name in BASE_SUBJECTS:
        if name in existing_names:
            print(f"⏩ Предмет уже существует: {name}")
            continue

        repo.create(
            name=name,
            teacher_id=TEACHER_TELEGRAM_ID
        )
        print(f"✅ Создан предмет: {name}")
        created += 1

    if created == 0:
        print("ℹ️ Все базовые предметы уже существуют.")
    else:
        print(f"🎉 Создано предметов: {created}")

    db.close()


if __name__ == "__main__":
    main()