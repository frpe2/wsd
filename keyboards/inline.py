from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cartridge_list_keyboard(cartridges, action):
    buttons = []
    for c in cartridges:
        buttons.append([
            InlineKeyboardButton(
                text=f"{c.model} ({c.status.value})",
                callback_data=f"{action}:{c.id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def cartridge_actions_keyboard(cid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit:{cid}"),
            InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete:{cid}")
        ],
        [
            InlineKeyboardButton(text="📜 История", callback_data=f"log:{cid}")
        ]
    ])