from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.db.database import Database
from app.db.repositories.submissions import SubmissionRepository
from app.db.repositories.users import UserRepository
from app.db.repositories.assignments import AssignmentRepository

from app.guards.student_group_guard import ensure_student_has_group
from app.keyboards.inline import assignments_keyboard

from app.states.student_states import SELECT_ASSIGNMENT, ENTER_SOLUTION
from app.utils.timezone import get_moscow_tzinfo

async def show_assignments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_student_has_group(update, context):
        return

    db = Database()
    user_repo = UserRepository(db)
    assignment_repo = AssignmentRepository(db)
    submission_repo = SubmissionRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)
    assignments = assignment_repo.get_by_group(user["group_id"])

    if not assignments:
        await update.message.reply_text("Заданий для вашей группы пока нет.")
        db.close()
        return

    text = "📚 Задания для вашей группы:\n\n"
    for a in assignments:
        text += f"📌 {a['title']}\n{a['description']}\n\n"
        deadline = None
        if a["deadline"]:
            try:
                deadline = datetime.strptime(a["deadline"], "%Y-%m-%d %H:%M %z")
                display_deadline = deadline.astimezone(
                    get_moscow_tzinfo()
                ).strftime("%Y-%m-%d %H:%M MSK")
            except ValueError:
                display_deadline = a["deadline"]

            text += f"⏰ Дедлайн: {display_deadline}\n\n"

        if deadline and not submission_repo.exists(a["id"], user["telegram_id"]):
            time_left = deadline - datetime.now(get_moscow_tzinfo())
            if time_left > timedelta(hours=22):
                await update.message.reply_text(
                    "⏳ Напоминание: до дедлайна по заданию "
                    f"«{a['title']}» ещё есть время ({display_deadline})."
                )

    await update.message.reply_text(text)
    db.close()

async def start_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_student_has_group(update, context):
        return ConversationHandler.END

    db = Database()
    user_repo = UserRepository(db)
    assignment_repo = AssignmentRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)
    assignments = assignment_repo.get_by_group(user["group_id"])

    if not assignments:
        await update.message.reply_text(
            "📭 Для вашей группы пока нет заданий."
        )
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

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    user_repo = UserRepository(db)

    user = user_repo.get_by_telegram_id(update.effective_user.id)
    db.close()

    text = (
        "👤 *Ваш профиль*\n\n"
        f"ID: `{user['telegram_id']}`\n"
        f"Имя: {user['first_name'] or '—'}\n"
        f"Фамилия: {user['last_name'] or '—'}\n"
    )

    if user["group_id"]:
        text += "\n👥 Группа назначена"
    else:
        text += "\n❗ Группа не назначена"

    await update.message.reply_text(text, parse_mode="Markdown")
