from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, t
from services.currency_display import get_currency_flag, get_currency_label


def get_rates_menu_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="USD", callback_data="rate_currency:USD")],
        [InlineKeyboardButton(text="EUR", callback_data="rate_currency:EUR")],
        [InlineKeyboardButton(text="RUB", callback_data="rate_currency:RUB")],
        [InlineKeyboardButton(text=t("btn_all_currencies", lang), callback_data="all_rates")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_dynamic_rates_menu_keyboard(codes: list[str], lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for code in codes:
        text = f"{get_currency_flag(code)} {get_currency_label(code, lang)}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"rate_currency:{code}")])
    buttons.append([InlineKeyboardButton(text=t("btn_all_currencies", lang), callback_data="all_rates")])
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_all_currencies_keyboard(codes: list[str], lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for code in codes:
        text = f"{get_currency_flag(code)} {get_currency_label(code, lang)}"
        row.append(InlineKeyboardButton(text=text, callback_data=f"rate_currency:{code}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text=t("btn_main_currencies", lang), callback_data="rates")])
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_currency_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return get_rates_menu_keyboard(lang)


def get_rate_detail_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_booking", lang), callback_data="booking"), InlineKeyboardButton(text=t("btn_individual", lang), callback_data="individual_rate")],
        [InlineKeyboardButton(text=t("btn_to_currency_list", lang), callback_data="rates")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
    ])
