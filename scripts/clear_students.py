import sys
from pathlib import Path
from app.db.database import Database

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

def main():
    db = Database()

    db.execute(
        """
        DELETE FROM submissions
        WHERE student_id IN (
            SELECT telegram_id FROM users WHERE role = 'student'
        )
        """
    )
    db.execute("DELETE FROM users WHERE role = 'student'")

    db.close()
    print("✅ Студенты и их решения очищены. Преподаватель сохранён.")


if __name__ == "__main__":
    main()
