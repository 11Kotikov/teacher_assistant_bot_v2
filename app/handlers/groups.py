from telegram import Update
from telegram.ext import ContextTypes

from app.db.database import Database
from app.services.users_service import UsersService
from app.keyboards.groups import groups_keyboard
from app.keyboards.main_menu import STUDENT_MENU


async def choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    service = UsersService(db)

    groups = service.groups.get_all()

    if not groups:
        await update.message.reply_text(
            "❗ Пока нет доступных групп. Обратитесь к преподавателю."
        )
        return

    await update.message.reply_text(
        "Выберите вашу группу:",
        reply_markup=groups_keyboard(groups),
    )


async def set_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    group_name = update.message.text

    db = Database()
    service = UsersService(db)

    success = service.set_user_group(telegram_id, group_name)

    if success:
        await update.message.reply_text(
            f"✅ Группа «{group_name}» установлена",
            reply_markup=STUDENT_MENU,
        )
    else:
        await update.message.reply_text(
            "❌ Такой группы не существует"
        )