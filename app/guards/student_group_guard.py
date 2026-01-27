from telegram import Update
from telegram.ext import ContextTypes

from app.db.database import Database
from app.db.repositories.users import UserRepository


async def ensure_student_has_group(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    db = Database()
    repo = UserRepository(db)

    user = repo.get_by_telegram_id(update.effective_user.id)
    db.close()

    if not user or not user["group_id"]:
        await update.message.reply_text(
            "❗ Вы ещё не прикреплены к группе.\n"
            "Обратитесь к преподавателю."
        )
        return False

    return True
