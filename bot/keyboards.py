from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Текущие курсы", callback_data="rates"),
            InlineKeyboardButton(text="💱 Конвертер", callback_data="convert")
        ],
        [
            InlineKeyboardButton(text="🔔 Подписка", callback_data="subscribe"),
            InlineKeyboardButton(text="🎯 Целевой курс", callback_data="target")
        ],
        [
            InlineKeyboardButton(text="💰 Обмен", callback_data="exchange")
        ]
    ])
