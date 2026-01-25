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
from app.handlers.auth import start, set_role

from app.handlers.student import (
    show_assignments, 
    start_submit, 
    select_assignment,
    enter_solution,
)

from app.states.student_states import SELECT_ASSIGNMENT, ENTER_SOLUTION


from app.handlers.teacher import (
    start_create_assignment,
    select_subject,
    select_group,
    enter_title,
    enter_description
)

from app.states.teacher_states import (
    SELECT_SUBJECT,
    SELECT_GROUP,
    ENTER_TITLE,
    ENTER_DESCRIPTION,
)

from app.guards.role_guard import role_required

from app.handlers.teacher_review import (
    select_review_assignment,
    start_review_submissions,
    select_review_group,
)

from app.states.teacher_review_states import (
    SELECT_REVIEW_GROUP,
    SELECT_REVIEW_ASSIGNMENT,
)

def main() -> None:
    validate_config()
    setup_logging(Config.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("Bot starting...")

    app = Application.builder().token(Config.BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
 
    # FSM преподавателя
    teacher_conv = ConversationHandler(
        entry_points=[
            CommandHandler("create_assignment", start_create_assignment),
            MessageHandler(
                filters.Regex("^➕ Создать задание$"),
                start_create_assignment,
            ),
        ],
        states={
            SELECT_SUBJECT: [
                CallbackQueryHandler(select_subject, pattern="^subject_"),
            ],
            SELECT_GROUP: [
                CallbackQueryHandler(select_group, pattern="^group_"),
            ],
            ENTER_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_title),
            ],
            ENTER_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_description),
            ],
        },
        fallbacks=[],
    )

    review_conv = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^📂 Проверить работы$"),
                start_review_submissions,
            ),
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

    app.add_handler(review_conv)
    app.add_handler(teacher_conv)
    
    # FSM студента
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

    app.add_handler(student_conv)


    # Выбор роли (кнопки)
    role_filter = filters.Regex("^(👨‍🎓 Студент|👨‍🏫 Преподаватель)$")
    app.add_handler(MessageHandler(role_filter, set_role))

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