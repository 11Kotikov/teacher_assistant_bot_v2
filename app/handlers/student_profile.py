from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.services.users_service import UsersService
from app.states.student_profile_states import (
    ENTER_FIRST_NAME,
    ENTER_LAST_NAME,
)


async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Добро пожаловать!\n\nВведите ваше имя:")
    return ENTER_FIRST_NAME


async def set_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["first_name"] = update.message.text.strip()
    await update.message.reply_text("Введите вашу фамилию:")
    return ENTER_LAST_NAME


async def set_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["last_name"] = update.message.text.strip()
    return await finish_registration(update, context)


async def finish_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = context.user_data["first_name"]
    last_name = context.user_data["last_name"]

    db = Database()
    service = UsersService(db)
    service.update_profile(
        update.effective_user.id,
        first_name,
        last_name,
    )
    db.close()

    context.user_data.clear()

    await update.message.reply_text(
        "✅ Профиль заполнен!\n\n"
        "⏳ Ожидайте назначения в группу преподавателем."
    )

    return ConversationHandler.END