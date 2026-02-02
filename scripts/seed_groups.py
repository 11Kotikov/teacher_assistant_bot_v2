import sys
from pathlib import Path

# 👇 добавляем корень проекта в PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.database import Database
from app.db.repositories.groups import GroupRepository


GROUPS = [
    "ИТ-15",
    "Р-11 + Э-14",
    "Р-12 + Ю-13",
    "ИТ-25",
    "Р-21",
    "Р-22",
    "Ю-23",
    "Э-24",
    "ИТ-35",
]


def main():
    db = Database()
    repo = GroupRepository(db)

    for name in GROUPS:
        repo.create(name)
        print(f"✔ Группа добавлена: {name}")

    db.close()
    print("✅ Группы успешно инициализированы")


if __name__ == "__main__":
    main()