from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from app.db.database import Database
from app.db.repositories.users import UserRepository


def role_required(required_role: str):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            db = Database()
            repo = UserRepository(db)

            user = repo.get_by_telegram_id(update.effective_user.id)
            db.close()

            if not user or user["role"] != required_role:
                await update.message.reply_text(
                    "⛔ Эта команда только для преподавателей."
                    if required_role == "teacher"
                    else "⛔ Эта команда только для студентов."
                )
                return

            return await handler(update, context)

        return wrapper
    return decorator