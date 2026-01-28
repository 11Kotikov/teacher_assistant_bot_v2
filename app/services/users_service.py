from app.db.database import Database
from app.db.repositories.users import UserRepository
from app.db.repositories.groups import GroupRepository

class UsersService:
    def __init__(self, db: Database):
        self.repo = UserRepository(db)

    def get_or_create_user(self, telegram_id: int) -> dict:
        user = self.repo.get_by_telegram_id(telegram_id)
        if user:
            return user

        self.repo.create(telegram_id)
        return self.repo.get_by_telegram_id(telegram_id)

    def is_student_profile_complete(self, user: dict) -> bool:
        return bool(user["first_name"] and user["last_name"])

    def update_profile(self, telegram_id: int, first_name: str, last_name: str):
        self.repo.update_profile(telegram_id, first_name, last_name)