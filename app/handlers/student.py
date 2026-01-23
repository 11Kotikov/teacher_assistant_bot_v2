from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.repositories.submissions import SubmissionRepository
from app.db.repositories.users import UserRepository
from app.db.repositories.assignments import AssignmentRepository
from app.db.database import Database

from app.keyboards.inline import assignments_keyboard

from app.states.student_states import SELECT_ASSIGNMENT
from app.states.student_states import ENTER_SOLUTION


async def show_assignments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()

    user_repo = UserRepository(db)
    assignment_repo = AssignmentRepository(db)

    telegram_id = update.effective_user.id
    user = user_repo.get_by_telegram_id(telegram_id)

    if not user or not user["group_id"]:
        await update.message.reply_text(
            "❗ Вам не назначена группа. Обратитесь к преподавателю."
        )
        db.close()
        return

    assignments = assignment_repo.get_by_group(user["group_id"])

    if not assignments:
        await update.message.reply_text("Заданий для вашей группы пока нет.")
        db.close()
        return

    text = "📚 Задания для вашей группы:\n\n"
    for a in assignments:
        text += f"📌 {a['title']}\n{a['description']}\n\n"

    await update.message.reply_text(text)
    db.close()
    
async def start_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    user_repo = UserRepository(db)
    assignment_repo = AssignmentRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)

    if not user or not user["group_id"]:
        await update.message.reply_text(
            "❗ Вам не назначена группа."
        )
        db.close()
        return ConversationHandler.END

    assignments = assignment_repo.get_by_group(user["group_id"])

    if not assignments:
        await update.message.reply_text("Для вашей группы нет заданий.")
        db.close()
        return ConversationHandler.END

    await update.message.reply_text(
        "📌 Выберите задание:",
        reply_markup=assignments_keyboard(assignments),
    )

    db.close()
    return SELECT_ASSIGNMENT

async def select_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    assignment_id = int(query.data.split("_")[1])
    context.user_data["assignment_id"] = assignment_id

    await query.edit_message_text("✏️ Введите ваше решение:")
    return ENTER_SOLUTION

async def enter_solution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    solution_text = update.message.text

    db = Database()
    submission_repo = SubmissionRepository(db)

    assignment_id = context.user_data["assignment_id"]
    student_id = update.effective_user.id

    if submission_repo.exists(assignment_id, student_id):
        await update.message.reply_text("❌ Вы уже сдали это задание.")
        db.close()
        context.user_data.clear()
        return ConversationHandler.END

    submission_repo.create(
        assignment_id=assignment_id,
        student_id=student_id,
        text=solution_text,
    )

    db.close()

    await update.message.reply_text("✅ Решение отправлено!")

    context.user_data.clear()
    return ConversationHandler.END