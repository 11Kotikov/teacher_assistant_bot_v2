import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.db.database import Database

def main():
    db = Database()

    # db.execute("DELETE FROM reviews")
    db.execute("DELETE FROM submissions")
    db.execute("DELETE FROM assignments")

    db.close()
    print("✅ Задания, решения и проверки очищены.")


if __name__ == "__main__":
    main()
