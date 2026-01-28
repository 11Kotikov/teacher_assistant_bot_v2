from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from app.db.database import Database
from app.services.users_service import UsersService

from app.keyboards.main_menu import STUDENT_MENU, TEACHER_MENU

ROLE_KEYBOARD = ReplyKeyboardMarkup(
    [["👨‍🎓 Студент", "👨‍🏫 Преподаватель"]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db = Database()
    service = UsersService(db)

    telegram_id = update.effective_user.id
    user = service.get_or_create_user(telegram_id)

    # 1️⃣ Роль не выбрана
    if user["role"] is None:
        await update.message.reply_text(
            "👋 Привет! Выберите вашу роль:",
            reply_markup=ROLE_KEYBOARD,
        )
        db.close()
        return

    # 2️⃣ Студент
    if user["role"] == "student":
        if user["first_name"] is None or user["last_name"] is None:
            await update.message.reply_text(
                "✍️ Давайте заполним профиль."
            )
            db.close()
            await context.bot.send_message(
                chat_id=telegram_id,
                text="Введите имя:"
            )
            return

        await update.message.reply_text(
            "👋 С возвращением, студент!",
            reply_markup=STUDENT_MENU,
        )

    # 3️⃣ Преподаватель
    elif user["role"] == "teacher":
        await update.message.reply_text(
            "👋 С возвращением, преподаватель!",
            reply_markup=TEACHER_MENU,
        )

    db.close()


async def set_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    telegram_id = update.effective_user.id

    role_map = {
        "👨‍🎓 Студент": "student",
        "👨‍🏫 Преподаватель": "teacher",
    }

    if text not in role_map:
        return

    menu = STUDENT_MENU if role_map[text] == "student" else TEACHER_MENU
    
    await update.message.reply_text(
    f"✅ Роль установлена: {role_map[text]}",
    reply_markup=menu,
    )
    
    db = Database()
    service = UsersService(db)
    service.set_role(telegram_id, role_map[text])
