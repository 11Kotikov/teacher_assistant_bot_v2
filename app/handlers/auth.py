# auth.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.config import Config
from app.db.database import Database
from app.services.users_service import UsersService
from app.handlers.student_profile import start_registration
from app.keyboards.main_menu import (
    STUDENT_MENU,
    STUDENT_NO_GROUP_MENU,
    TEACHER_MENU,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    # ---------- TEACHER ----------
    if telegram_id == Config.TEACHER_TELEGRAM_ID:
        db = Database()
        service = UsersService(db)
        service.get_or_create_user(telegram_id)
        db.close()
        await update.message.reply_text(
            "👋 С возвращением, преподаватель!",
            reply_markup=TEACHER_MENU,
        )
        return ConversationHandler.END

    # ---------- STUDENT ----------
    db = Database()
    service = UsersService(db)
    user = service.get_or_create_user(telegram_id)

    # ❗ ЕСЛИ ПРОФИЛЬ НЕ ЗАПОЛНЕН — ЗАПУСКАЕМ РЕГИСТРАЦИЮ
    if user["first_name"] is None or user["last_name"] is None:
        db.close()
        return await start_registration(update, context)

    # профиль есть, но группы нет
    if user["group_id"] is None:
        await update.message.reply_text(
            "⏳ Вы ещё не назначены в группу.\n\n"
            "📌 Обратитесь к преподавателю или дождитесь назначения.",
            reply_markup=STUDENT_NO_GROUP_MENU,
        )
        db.close()
        return ConversationHandler.END

    # всё готово
    await update.message.reply_text(
        "👋 С возвращением!",
        reply_markup=STUDENT_MENU,
    )
    db.close()
    return ConversationHandler.END
