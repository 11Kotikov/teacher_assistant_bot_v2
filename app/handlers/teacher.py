from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database

from app.db.repositories.assignments import AssignmentRepository
from app.db.repositories.subjects import SubjectRepository
from app.db.repositories.groups import GroupRepository
from app.db.repositories.users import UserRepository  # ← добавь импорт


from app.states.teacher_states import (
    ENTER_DEADLINE,
    ENTER_DESCRIPTION,
    ENTER_TITLE,
    SELECT_SUBJECT,
    SELECT_GROUP,
)

from app.keyboards.inline import subjects_keyboard, groups_keyboard



async def start_create_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    
    user_repo = UserRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)

    if not user or user["role"] != "teacher":
        await update.message.reply_text("⛔ У вас нет прав на эту команду.")
        db.close()
        return ConversationHandler.END
    
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

async def enter_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.text
    context.user_data["description"] = description

    await update.message.reply_text(
        "⏰ Введите дедлайн в формате YYYY-MM-DD HH:MM (например, 2025-03-31 18:00):"
    )
    return ENTER_DEADLINE


async def enter_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_deadline = update.message.text.strip()
    try:
        deadline = datetime.strptime(raw_deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text(
            "❗ Некорректный формат. Используйте YYYY-MM-DD HH:MM (например, 2025-03-31 18:00)."
        )
        return ENTER_DEADLINE

    context.user_data["deadline"] = deadline.strftime("%Y-%m-%d %H:%M")

    db = Database()
    assignment_repo = AssignmentRepository(db)

    assignment_repo.create(
        title=context.user_data["title"],
        description=context.user_data["description"],
        deadline=context.user_data["deadline"],
        subject_id=context.user_data["subject_id"],
        group_id=context.user_data["group_id"],
    )

    db.close()

    await update.message.reply_text("✅ Задание успешно создано!")

    context.user_data.clear()
    return ConversationHandler.END