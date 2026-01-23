from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.states.teacher_states import ENTER_TITLE, SELECT_SUBJECT, SELECT_GROUP
from app.keyboards.inline import subjects_keyboard, groups_keyboard
from app.db.database import Database
from app.db.repositories.subjects import SubjectRepository
from app.db.repositories.groups import GroupRepository


async def start_create_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    subject_repo = SubjectRepository(db)

    teacher_id = update.effective_user.id
    subjects = subject_repo.get_by_teacher(teacher_id)

    if not subjects:
        await update.message.reply_text(
            "У вас нет предметов. Сначала создайте предмет."
        )
        db.close()
        return ConversationHandler.END

    await update.message.reply_text(
        "Выберите предмет:",
        reply_markup=subjects_keyboard(subjects),
    )

    db.close()
    return SELECT_SUBJECT


async def select_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject_id = int(query.data.split("_")[1])
    context.user_data["subject_id"] = subject_id

    db = Database()
    group_repo = GroupRepository(db)
    groups = group_repo.get_all()

    await query.edit_message_text(
        "Выберите группу:",
        reply_markup=groups_keyboard(groups),
    )

    db.close()
    return SELECT_GROUP


async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_id = int(query.data.split("_")[1])
    context.user_data["group_id"] = group_id

    await query.edit_message_text("✏️ Введите название задания:")
    return ENTER_TITLE

async def enter_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text
    context.user_data["title"] = title

    await update.message.reply_text(
        "📝 Введите описание задания:"
    )

    return ENTER_DESCRIPTION