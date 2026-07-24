from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_rates_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="USD", callback_data="rate_currency:USD")],
        [InlineKeyboardButton(text="EUR", callback_data="rate_currency:EUR")],
        [InlineKeyboardButton(text="RUB", callback_data="rate_currency:RUB")],
        [InlineKeyboardButton(text="Все валюты", callback_data="all_rates")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_dynamic_rates_menu_keyboard(codes: list[str]) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for code in codes:
        buttons.append([InlineKeyboardButton(text=code, callback_data=f"rate_currency:{code}")])
    buttons.append([InlineKeyboardButton(text="Все валюты", callback_data="all_rates")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_currency_keyboard() -> InlineKeyboardMarkup:
    return get_rates_menu_keyboard()
