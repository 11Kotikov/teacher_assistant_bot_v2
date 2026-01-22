import signal
import sys
import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import filters

from app.config import Config, validate_config
from app.logging import setup_logging
from app.handlers.auth import start, set_role

def main() -> None:
    validate_config()
    setup_logging(Config.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("Bot starting...")

    app = Application.builder().token(Config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_role))

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