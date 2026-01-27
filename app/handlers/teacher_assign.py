from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.db.repositories.groups import GroupRepository
from app.db.repositories.users import UserRepository

from app.keyboards.inline import groups_keyboard, students_keyboard

from app.states.teacher_assign_states import SELECT_ASSIGN_GROUP, SELECT_ASSIGN_STUDENT


async def start_assign_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    group_repo = GroupRepository(db)

    groups = group_repo.get_all()
    db.close()

    if not groups:
        await update.message.reply_text("❗ Группы не найдены.")
        return ConversationHandler.END

    await update.message.reply_text(
        "👥 Выберите группу:",
        reply_markup=groups_keyboard(groups),
    )

    return SELECT_ASSIGN_GROUP


async def select_assign_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_id = int(query.data.split("_")[1])
    context.user_data["assign_group_id"] = group_id

    db = Database()
    user_repo = UserRepository(db)

    students = user_repo.get_students_without_group()
    db.close()

    if not students:
        await query.edit_message_text(
            "✅ Все студенты уже распределены по группам."
        )
        return ConversationHandler.END

    await query.edit_message_text(
        "👤 Выберите студента:",
        reply_markup=students_keyboard(students),
    )
    return SELECT_ASSIGN_STUDENT

async def select_assign_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    student_id = int(query.data.split("_")[1])
    group_id = context.user_data["assign_group_id"]

    db = Database()
    user_repo = UserRepository(db)
    group_repo = GroupRepository(db)

    user = user_repo.get_by_telegram_id(student_id)
    if user["group_id"]:
        await query.edit_message_text("⚠️ Студент уже состоит в группе.")
        db.close()
        context.user_data.clear()
        return ConversationHandler.END

    user_repo.assign_to_group(student_id, group_id)
    group = group_repo.get_by_id(group_id)
    db.close()

    try:
        await context.bot.send_message(
            chat_id=student_id,
            text=(
                f"✅ Вас добавили в группу *{group['name']}*\n\n"
                "📚 Теперь вам доступны задания.\n"
                "Используйте команду /submit"
            ),
            parse_mode="Markdown",
        )
    except Exception:
        pass

    await query.edit_message_text("✅ Студент успешно назначен в группу.")
    context.user_data.clear()
    return ConversationHandler.END