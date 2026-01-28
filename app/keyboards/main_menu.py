from telegram import ReplyKeyboardMarkup

STUDENT_MENU = ReplyKeyboardMarkup(
    [
        ["📚 Мои задания"],
        ["📝 Сдать работу"],
        ["📊 Мои оценки"],
        ["👤 Профиль"],
    ],
    resize_keyboard=True,
)

TEACHER_MENU = ReplyKeyboardMarkup(
    [
        ["➕ Создать задание"],
        ["📂 Проверить работы"],
        ["👥 Группы"],
        ["➕ Назначить студента"],
    ],
    resize_keyboard=True,
)
