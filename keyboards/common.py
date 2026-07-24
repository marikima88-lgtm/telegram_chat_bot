from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="main_menu")]])


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    from keyboards.main import get_main_menu_keyboard as main_menu
    return main_menu()
