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

STUDENT_NO_GROUP_MENU = ReplyKeyboardMarkup(
    [
        ["👤 Профиль"],
        ["ℹ️ Почему нет заданий?"],
    ],
    resize_keyboard=True,
)

from telegram import ReplyKeyboardMarkup

STUDENT_PROFILE_REQUIRED_MENU = ReplyKeyboardMarkup(
    [
        ["📝 Заполнить профиль"],
    ],
    resize_keyboard=True,
)