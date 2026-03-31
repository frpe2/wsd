from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu(is_admin=False):
    keyboard = [
        [KeyboardButton(text="📦 Список картриджей")],
        [KeyboardButton(text="🔍 Поиск")],
        [KeyboardButton(text="📊 Фильтр по статусу")],
    ]

    if is_admin:
        keyboard += [
            [KeyboardButton(text="➕ Добавить картридж")],
            [KeyboardButton(text="📤 В сервис")],
            [KeyboardButton(text="📥 Из сервиса")],
        ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)