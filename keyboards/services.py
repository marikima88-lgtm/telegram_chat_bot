from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, t
from services.currency_display import CURRENCY_FLAGS, get_currency_flag, get_currency_label, sort_currency_codes


def get_currency_picker_keyboard(prefix: str, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    codes = sort_currency_codes(CURRENCY_FLAGS.keys())
    buttons: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for code in codes:
        row.append(
            InlineKeyboardButton(
                text=f"{get_currency_flag(code)} {get_currency_label(code, lang)}",
                callback_data=f"{prefix}:{code}",
            )
        )
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_booking_keyboard(mode: str | None = None, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    if mode == "currency":
        buttons = [
            [InlineKeyboardButton(text="USD", callback_data="booking_currency:USD")],
            [InlineKeyboardButton(text="EUR", callback_data="booking_currency:EUR")],
            [InlineKeyboardButton(text="RUB", callback_data="booking_currency:RUB")],
            [InlineKeyboardButton(text=t("btn_other_currency", lang), callback_data="booking_currency:OTHER")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    elif mode == "nominals":
        buttons = [
            [InlineKeyboardButton(text=t("no", lang), callback_data="booking_nominals:no")],
            [InlineKeyboardButton(text=t("btn_nominals_yes", lang), callback_data="booking_nominals:yes")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    elif mode == "review":
        buttons = [
            [InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="confirm_booking")],
            [InlineKeyboardButton(text=t("btn_edit", lang), callback_data="main_menu")],
            [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text=t("btn_buy_currency", lang), callback_data="booking_op:buy")],
            [InlineKeyboardButton(text=t("btn_sell_currency", lang), callback_data="booking_op:sell")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_individual_rate_keyboard(mode: str | None = None, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    if mode == "currency":
        buttons = [
            [InlineKeyboardButton(text="USD", callback_data="rate_req_currency:USD")],
            [InlineKeyboardButton(text="EUR", callback_data="rate_req_currency:EUR")],
            [InlineKeyboardButton(text="RUB", callback_data="rate_req_currency:RUB")],
            [InlineKeyboardButton(text=t("btn_other_currency", lang), callback_data="rate_req_currency:OTHER")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    elif mode == "review":
        buttons = [
            [InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="confirm_individual")],
            [InlineKeyboardButton(text=t("btn_edit", lang), callback_data="main_menu")],
            [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text=t("btn_buy", lang), callback_data="rate_req_op:buy")],
            [InlineKeyboardButton(text=t("btn_sell", lang), callback_data="rate_req_op:sell")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
