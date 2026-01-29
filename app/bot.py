import signal
import sys
import logging

from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

from app.config import Config, validate_config
from app.logging import setup_logging
from app.handlers.auth import start

# ---------- STUDENT ----------
from app.handlers.student import (
    show_assignments,
    show_profile,
    start_submit,
    select_assignment,
    enter_solution,
)

from app.states.student_states import (
    SELECT_ASSIGNMENT,
    ENTER_SOLUTION,
)

from app.handlers.student_profile import (
    set_first_name,
    set_last_name,
)

from app.states.student_profile_states import (
    ENTER_FIRST_NAME,
    ENTER_LAST_NAME,
)

# ---------- TEACHER: CREATE ASSIGNMENT ----------
from app.handlers.teacher import (
    start_create_assignment,
    select_subject,
    select_group as select_assignment_group,
    enter_title,
    enter_description,
    enter_deadline,
)

from app.states.teacher_states import (
    SELECT_SUBJECT,
    SELECT_GROUP as SELECT_ASSIGNMENT_GROUP,
    ENTER_TITLE,
    ENTER_DESCRIPTION,
    ENTER_DEADLINE,
)

# ---------- TEACHER: REVIEW ----------
from app.handlers.teacher_review import (
    start_review_submissions,
    select_review_group,
    select_review_assignment,
)

from app.states.teacher_review_states import (
    SELECT_REVIEW_GROUP,
    SELECT_REVIEW_ASSIGNMENT,
)

# ---------- TEACHER: GROUPS ----------
from app.handlers.teacher_groups import (
    start_groups,
    select_group as select_groups_group,
)

from app.states.teacher_groups_states import (
    SELECT_GROUP as SELECT_GROUPS_GROUP,
)

# ---------- TEACHER: ASSIGN STUDENT ----------
from app.handlers.teacher_assign import (
    start_assign_student,
    select_assign_group,
    select_assign_student,
)

from app.states.teacher_assign_states import (
    SELECT_ASSIGN_GROUP,
    SELECT_ASSIGN_STUDENT
)

def main() -> None:
    validate_config()
    setup_logging(Config.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("Bot starting...")

    app = Application.builder().token(Config.BOT_TOKEN).build()

    # ---------- CREATE ASSIGNMENT FSM ----------
    teacher_conv = ConversationHandler(
        entry_points=[
            CommandHandler("create_assignment", start_create_assignment),
            MessageHandler(filters.Regex("^➕ Создать задание$"), start_create_assignment),
        ],
        states={
            SELECT_SUBJECT: [
                CallbackQueryHandler(select_subject, pattern="^subject_"),
            ],
            SELECT_ASSIGNMENT_GROUP: [
                CallbackQueryHandler(select_assignment_group, pattern="^group_"),
            ],
            ENTER_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_title),
            ],
            ENTER_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_description),
            ],
            ENTER_DEADLINE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_deadline),
            ],
        },
        fallbacks=[],
    )

    # ---------- REVIEW FSM ----------
    review_conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📂 Проверить работы$"), start_review_submissions),
        ],
        states={
            SELECT_REVIEW_GROUP: [
                CallbackQueryHandler(select_review_group, pattern="^group_"),
            ],
            SELECT_REVIEW_ASSIGNMENT: [
                CallbackQueryHandler(select_review_assignment, pattern="^assignment_"),
            ],
        },
        fallbacks=[],
    )

    # ---------- GROUPS FSM ----------
    groups_conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^👥 Группы$"), start_groups),
        ],
        states={
            SELECT_GROUPS_GROUP: [
                CallbackQueryHandler(select_groups_group, pattern="^group_"),
            ],
        },
        fallbacks=[],
    )

    # ---------- ASSIGN STUDENT FSM (D3.1) ----------
    assign_student_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^➕ Назначить студента$"), start_assign_student)
    ],
    states={
        SELECT_ASSIGN_GROUP: [
            CallbackQueryHandler(select_assign_group, pattern="^group_"),
        ],
        SELECT_ASSIGN_STUDENT: [
            CallbackQueryHandler(select_assign_student, pattern="^student_"),
        ],
    },
    fallbacks=[],
)
    
    # ---------- STUDENT MENU HANDLERS ----------

    app.add_handler(
        MessageHandler(
            filters.Regex("^📚 Мои задания$"),
            show_assignments,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^📝 Сдать работу$"),
            start_submit,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^👤 Профиль$"),
            show_profile,
        )
    )

    # ---------- STUDENT FSM ----------
    student_conv = ConversationHandler(
        entry_points=[CommandHandler("submit", start_submit)],
        states={
            SELECT_ASSIGNMENT: [
                CallbackQueryHandler(select_assignment, pattern="^assignment_"),
            ],
            ENTER_SOLUTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_solution),
            ],
        },
        fallbacks=[],
    )
    
    student_profile_conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            ENTER_FIRST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_first_name),
            ],
            ENTER_LAST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_last_name),
            ],
        },
        fallbacks=[],
    )

    # Register FSMs
    app.add_handler(student_profile_conv)
    app.add_handler(teacher_conv)
    app.add_handler(review_conv)
    app.add_handler(groups_conv)
    app.add_handler(assign_student_conv)
    app.add_handler(student_conv)

    def shutdown(signum, frame):
        logger.info("Bot stopping...")
        app.stop()
        app.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    app.run_polling()

if __name__ == "__main__":
    main()