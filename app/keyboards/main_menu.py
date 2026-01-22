from telegram import ReplyKeyboardMarkup

STUDENT_MENU = ReplyKeyboardMarkup(
    [
        ["📚 Мои задания"],
        ["📝 Сдать работу"],
        ["📊 Мои оценки"],
    ],
    resize_keyboard=True,
)

TEACHER_MENU = ReplyKeyboardMarkup(
    [
        ["➕ Создать задание"],
        ["📂 Проверить работы"],
        ["👥 Группы"],
    ],
    resize_keyboard=True,
)
