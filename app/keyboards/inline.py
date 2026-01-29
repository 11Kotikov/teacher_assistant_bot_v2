from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def subjects_keyboard(subjects):
    keyboard = [
        [InlineKeyboardButton(text=s["name"], callback_data=f"subject_{s['id']}")]
        for s in subjects
    ]
    return InlineKeyboardMarkup(keyboard)

def subject_filter_keyboard(subjects, prefix: str):
    keyboard = [
        [InlineKeyboardButton(text=s["name"], callback_data=f"{prefix}{s['id']}")]
        for s in subjects
    ]
    return InlineKeyboardMarkup(keyboard)

def review_subjects_keyboard(subjects):
    return subject_filter_keyboard(subjects, "review_subject_")

def student_subjects_keyboard(subjects):
    return subject_filter_keyboard(subjects, "student_subject_")

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

def students_keyboard(students):
    keyboard = []

    for s in students:
        name = " ".join(filter(None, [s["first_name"], s["last_name"]]))
        if not name:
            name = f"ID {s['telegram_id']}"

        keyboard.append([
            InlineKeyboardButton(
                name,
                callback_data=f"student_{s['telegram_id']}"
            )
        ])
    return InlineKeyboardMarkup(keyboard)
