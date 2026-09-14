from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, t


def get_contacts_keyboard(map_url: str | None = None, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    buttons = []
    if map_url:
        buttons.append([InlineKeyboardButton(text=t("btn_open_2gis", lang), url=map_url)])
    buttons.append([InlineKeyboardButton(text=t("btn_request_call", lang), callback_data="call_back")])
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
