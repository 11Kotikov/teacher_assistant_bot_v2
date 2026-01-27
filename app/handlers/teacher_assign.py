from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.db.repositories.groups import GroupRepository
from app.db.repositories.users import UserRepository
from app.keyboards.inline import groups_keyboard, students_keyboard
from app.states.teacher_assign_states import (
    SELECT_ASSIGN_GROUP,
    SELECT_ASSIGN_STUDENT,
)

async def start_assign_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    group_repo = GroupRepository(db)

    groups = group_repo.get_all()
    db.close()

    await update.message.reply_text(
        "👥 Выберите группу:",
        reply_markup=groups_keyboard(groups),
    )

    return SELECT_ASSIGN_GROUP


async def select_assign_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_id = int(query.data.split("_")[1])
    context.user_data["group_id"] = group_id

    db = Database()
    user_repo = UserRepository(db)
    students = user_repo.get_students_without_group()
    db.close()

    if not students:
        await query.edit_message_text("✅ Все студенты уже распределены по группам.")
        return ConversationHandler.END

    await query.edit_message_text(
        "👤 Выберите студента:",
        reply_markup=students_keyboard(students),
    )

    return SELECT_ASSIGN_STUDENT


async def select_assign_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    telegram_id = int(query.data.split("_")[1])
    group_id = context.user_data["group_id"]

    db = Database()
    user_repo = UserRepository(db)
    user_repo.set_group(telegram_id, group_id)
    db.close()

    await query.edit_message_text("✅ Студент успешно добавлен в группу.")

    context.user_data.clear()
    return ConversationHandler.END
