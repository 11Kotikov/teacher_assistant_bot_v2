from app.db.database import Database
from app.db.repositories.users import UserRepository
from app.db.repositories.groups import GroupRepository

class UsersService:
    def __init__(self, db: Database):
        self.repo = UserRepository(db)
        self.groups = GroupRepository(db)

    def get_or_create_user(self, telegram_id: int):
        user = self.repo.get_by_telegram_id(telegram_id)
        if user:
            return user

        self.repo.create(telegram_id)
        return self.repo.get_by_telegram_id(telegram_id)

    def set_role(self, telegram_id: int, role: str):
        self.repo.db.execute(
            "UPDATE users SET role = ? WHERE telegram_id = ?",
            (role, telegram_id),
        )
        
    def set_user_group(self, telegram_id: int, group_name: str):
        group = self.groups.get_by_name(group_name)
        if not group:
            return False
        self.repo.set_group(telegram_id, group["id"])
        return True
