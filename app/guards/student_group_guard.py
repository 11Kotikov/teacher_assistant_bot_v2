from telegram import Update
from telegram.ext import ContextTypes

from app.db.database import Database
from app.db.repositories.users import UserRepository


async def ensure_student_has_group(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    db = Database()
    user_repo = UserRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)
    db.close()

    if not user or not user["group_id"]:
        await update.message.reply_text(
            "❗ Вы пока *не назначены в группу*.\n\n"
            "📌 Что делать дальше:\n"
            "• Обратитесь к преподавателю\n"
            "• Или дождитесь, когда вас добавят в группу\n\n"
            "⏳ После этого задания появятся автоматически.",
            parse_mode="Markdown",
        )
        return False

    return True
