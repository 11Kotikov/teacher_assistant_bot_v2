import sys
from pathlib import Path

from app.db.database import Database

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

def main():
    db = Database()

    db.execute("DELETE FROM reviews")
    db.execute("DELETE FROM submissions")
    db.execute("DELETE FROM assignments")

    db.close()
    print("✅ Задания, решения и проверки очищены.")


if __name__ == "__main__":
    main()
