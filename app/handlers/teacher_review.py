from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database

from app.db.repositories.groups import GroupRepository
from app.db.repositories.assignments import AssignmentRepository
from app.db.repositories.submissions import SubmissionRepository
from app.db.repositories.users import UserRepository

from app.keyboards.inline import groups_keyboard, review_subjects_keyboard

from app.states.teacher_review_states import (
    SELECT_REVIEW_GROUP,
    SELECT_REVIEW_SUBJECT,
    SELECT_REVIEW_ASSIGNMENT,
)

from app.guards.role_guard import role_required

@role_required("teacher")
async def start_review_submissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    repo = GroupRepository(db)

    groups = repo.get_all()
    db.close()

    if not groups:
        await update.message.reply_text("Группы не найдены.")
        return ConversationHandler.END

    await update.message.reply_text(
        "👥 Выберите группу:",
        reply_markup=groups_keyboard(groups),
    )

    return SELECT_REVIEW_GROUP

async def select_review_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_id = int(query.data.split("_")[1])
    context.user_data["review_group_id"] = group_id

    db = Database()
    repo = AssignmentRepository(db)
    subjects = repo.get_subjects_by_group(
        group_id,
        teacher_id=update.effective_user.id,
    )
    db.close()

    if not subjects:
        await query.edit_message_text("Для этой группы нет заданий по вашим предметам.")
        return ConversationHandler.END

    await query.edit_message_text(
        "📚 Выберите предмет:",
        reply_markup=review_subjects_keyboard(subjects),
    )

    return SELECT_REVIEW_SUBJECT

async def select_review_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject_id = int(query.data.split("_")[2])
    group_id = context.user_data["review_group_id"]

    db = Database()
    repo = AssignmentRepository(db)
    assignments = repo.get_by_group_and_subject(group_id, subject_id)
    db.close()

    if not assignments:
        await query.edit_message_text("Для этого предмета нет заданий.")
        return ConversationHandler.END

    from app.keyboards.inline import assignments_keyboard

    await query.edit_message_text(
        "📌 Выберите задание:",
        reply_markup=assignments_keyboard(assignments),
    )

    return SELECT_REVIEW_ASSIGNMENT

async def select_review_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    assignment_id = int(query.data.split("_")[1])

    db = Database()
    submission_repo = SubmissionRepository(db)
    user_repo = UserRepository(db)

    submissions = submission_repo.get_by_assignment(assignment_id)

    if not submissions:
        await query.edit_message_text("❌ Решений пока нет.")
        db.close()
        return ConversationHandler.END

    text = "📂 Сданные работы:\n\n"

    for s in submissions:
        user = user_repo.get_by_telegram_id(s["student_id"])
        date = s["created_at"]

        text += (
            f"👤 Студент: {user['telegram_id']}\n"
            f"🕒 Сдано: {date}\n"
            f"📝 Решение:\n{s['text']}\n"
            f"{'-'*20}\n"
        )

    db.close()

    await query.edit_message_text(text)
    context.user_data.clear()
    return ConversationHandler.END
