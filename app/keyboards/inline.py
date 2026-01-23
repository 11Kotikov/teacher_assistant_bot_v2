from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def subjects_keyboard(subjects):
    keyboard = [
        [InlineKeyboardButton(text=s["name"], callback_data=f"subject_{s['id']}")]
        for s in subjects
    ]
    return InlineKeyboardMarkup(keyboard)