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
from app.handlers.teacher import start_create_assignment, select_subject
from app.states.teacher_states import SELECT_SUBJECT, SELECT_GROUP

def main() -> None:
    validate_config()
    setup_logging(Config.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("Bot starting...")

    app = Application.builder().token(Config.BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))

    # FSM преподавателя
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("create_assignment", start_create_assignment)],
    states={
        SELECT_SUBJECT: [
            CallbackQueryHandler(select_subject, pattern="^subject_"),
        ],
    },
    fallbacks=[],
    )
    app.add_handler(conv_handler)

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