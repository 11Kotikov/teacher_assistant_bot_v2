from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.db.repositories.users import UserRepository
from app.states.student_profile_states import (
    ENTER_FIRST_NAME,
    ENTER_LAST_NAME,
)


async def start_student_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    user_repo = UserRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)
    db.close()

    # Если имя уже есть — профиль заполнен
    if user and user["first_name"] and user["last_name"]:
        return ConversationHandler.END

    await update.message.reply_text(
        "👋 Добро пожаловать!\n\n"
        "Для начала, напишите ваше *имя*:",
        parse_mode="Markdown",
    )

    return ENTER_FIRST_NAME


async def enter_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["first_name"] = update.message.text.strip()

    await update.message.reply_text(
        "Отлично! Теперь напишите вашу *фамилию*:",
        parse_mode="Markdown",
    )

    return ENTER_LAST_NAME


async def enter_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = context.user_data["first_name"]
    last_name = update.message.text.strip()

    db = Database()
    user_repo = UserRepository(db)

    user_repo.update_profile(
        telegram_id=update.effective_user.id,
        first_name=first_name,
        last_name=last_name,
    )

    db.close()
    context.user_data.clear()

    await update.message.reply_text(
        "✅ Профиль сохранён!\n\n"
        "⏳ Ожидайте назначения группы преподавателем."
    )

    return ConversationHandler.END