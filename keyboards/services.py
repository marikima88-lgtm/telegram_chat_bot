from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_booking_keyboard(mode: str | None = None) -> InlineKeyboardMarkup:
    if mode == "currency":
        buttons = [
            [InlineKeyboardButton(text="USD", callback_data="booking_currency:USD")],
            [InlineKeyboardButton(text="EUR", callback_data="booking_currency:EUR")],
            [InlineKeyboardButton(text="RUB", callback_data="booking_currency:RUB")],
            [InlineKeyboardButton(text="Другая валюта", callback_data="booking_currency:OTHER")],
        ]
    elif mode == "nominals":
        buttons = [
            [InlineKeyboardButton(text="Нет", callback_data="booking_nominals:Нет")],
            [InlineKeyboardButton(text="Да, указать пожелания", callback_data="booking_nominals:Да")],
        ]
    elif mode == "review":
        buttons = [
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_booking")],
            [InlineKeyboardButton(text="Изменить", callback_data="main_menu")],
            [InlineKeyboardButton(text="Отмена", callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Купить валюту", callback_data="booking_op:buy")],
            [InlineKeyboardButton(text="Продать валюту", callback_data="booking_op:sell")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_individual_rate_keyboard(mode: str | None = None) -> InlineKeyboardMarkup:
    if mode == "currency":
        buttons = [
            [InlineKeyboardButton(text="USD", callback_data="rate_req_currency:USD")],
            [InlineKeyboardButton(text="EUR", callback_data="rate_req_currency:EUR")],
            [InlineKeyboardButton(text="RUB", callback_data="rate_req_currency:RUB")],
            [InlineKeyboardButton(text="Другая валюта", callback_data="rate_req_currency:OTHER")],
        ]
    elif mode == "review":
        buttons = [
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_individual")],
            [InlineKeyboardButton(text="Изменить", callback_data="main_menu")],
            [InlineKeyboardButton(text="Отмена", callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Купить", callback_data="rate_req_op:buy")],
            [InlineKeyboardButton(text="Продать", callback_data="rate_req_op:sell")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
