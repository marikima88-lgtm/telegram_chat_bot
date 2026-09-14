from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, t


def get_alert_keyboard(mode: str | None = None, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    if mode == "confirm":
        buttons = [
            [InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="confirm_alert")],
            [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text=t("btn_create_alert", lang), callback_data="create_alert")],
            [InlineKeyboardButton(text=t("btn_disable_all", lang), callback_data="delete_all_alerts")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_alert_currency_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="USD", callback_data="alert_currency:USD")],
        [InlineKeyboardButton(text="EUR", callback_data="alert_currency:EUR")],
        [InlineKeyboardButton(text="RUB", callback_data="alert_currency:RUB")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
    ])


def get_alert_rate_type_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("rate_type_buy", lang), callback_data="alert_rate_type:buy")],
        [InlineKeyboardButton(text=t("rate_type_sell", lang), callback_data="alert_rate_type:sell")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
    ])


def get_alert_condition_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("condition_le", lang), callback_data="alert_condition:<=")],
        [InlineKeyboardButton(text=t("condition_ge", lang), callback_data="alert_condition:>=")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
    ])
