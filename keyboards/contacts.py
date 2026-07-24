from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_contacts_keyboard(map_url: str | None = None) -> InlineKeyboardMarkup:
    buttons = []
    if map_url:
        buttons.append([InlineKeyboardButton(text="🗺 Открыть в 2GIS", url=map_url)])
    buttons.append([InlineKeyboardButton(text="📞 Оставить заявку на звонок", callback_data="call_back")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
