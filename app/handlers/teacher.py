from telegram import Update
from telegram.ext import ContextTypes
from app.states.teacher_states import SELECT_SUBJECT


async def start_create_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Начинаем создание задания")
    return SELECT_SUBJECT