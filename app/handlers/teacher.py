from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.states.teacher_states import SELECT_SUBJECT, SELECT_GROUP
from app.keyboards.inline import subjects_keyboard
from app.db.database import Database
from app.db.repositories.subjects import SubjectRepository


async def start_create_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    repo = SubjectRepository(db)

    teacher_id = update.effective_user.id
    subjects = repo.get_by_teacher(teacher_id)

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

    await query.edit_message_text("Предмет выбран")
    return SELECT_GROUP