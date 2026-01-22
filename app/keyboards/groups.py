from telegram import ReplyKeyboardMarkup


def groups_keyboard(groups):
    buttons = [[g["name"]] for g in groups]

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
