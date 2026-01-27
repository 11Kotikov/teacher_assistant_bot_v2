from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.db.repositories.groups import GroupRepository
from app.db.repositories.users import UserRepository

from app.keyboards.inline import groups_keyboard

from app.states.teacher_groups_states import SELECT_GROUP, SHOW_STUDENTS
from app.guards.role_guard import role_required


@role_required("teacher")
async def start_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    return SELECT_GROUP


@role_required("teacher")
async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_id = int(query.data.split("_")[1])
    context.user_data["group_id"] = group_id

    db = Database()
    user_repo = UserRepository(db)
    students = user_repo.get_students_by_group(group_id)
    db.close()

    if not students:
        await query.edit_message_text(
            "❗ В этой группе пока нет студентов."
        )
        return ConversationHandler.END

    text = "👥 Студенты группы:\n\n"

    for s in students:
        name = " ".join(filter(None, [s["first_name"], s["last_name"]]))
        if not name:
            name = "❗ Имя не заполнено"

        text += (
            f"• {name}\n"
            f"  ID: {s['telegram_id']}\n\n"
        )

    await query.edit_message_text(text)

    return ConversationHandler.END
