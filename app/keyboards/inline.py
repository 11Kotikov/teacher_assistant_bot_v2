from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def subjects_keyboard(subjects):
    keyboard = [
        [InlineKeyboardButton(text=s["name"], callback_data=f"subject_{s['id']}")]
        for s in subjects
    ]
    return InlineKeyboardMarkup(keyboard)

def groups_keyboard(groups):
    keyboard = [
        [InlineKeyboardButton(g["name"], callback_data=f"group_{g['id']}")]
        for g in groups
    ]
    return InlineKeyboardMarkup(keyboard)

def assignments_keyboard(assignments):
    keyboard = [
        [InlineKeyboardButton(a["title"], callback_data=f"assignment_{a['id']}")]
        for a in assignments
    ]
    return InlineKeyboardMarkup(keyboard)
