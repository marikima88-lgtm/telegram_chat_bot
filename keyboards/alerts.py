from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_alert_keyboard(mode: str | None = None) -> InlineKeyboardMarkup:
    if mode == "confirm":
        buttons = [
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_alert")],
            [InlineKeyboardButton(text="Отмена", callback_data="main_menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Создать уведомление", callback_data="create_alert")],
            [InlineKeyboardButton(text="Отключить все", callback_data="delete_all_alerts")],
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_alert_currency_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="USD", callback_data="alert_currency:USD")],
        [InlineKeyboardButton(text="EUR", callback_data="alert_currency:EUR")],
        [InlineKeyboardButton(text="RUB", callback_data="alert_currency:RUB")],
    ])


def get_alert_rate_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Покупка", callback_data="alert_rate_type:buy")],
        [InlineKeyboardButton(text="Продажа", callback_data="alert_rate_type:sell")],
    ])


def get_alert_condition_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Не выше", callback_data="alert_condition:<=")],
        [InlineKeyboardButton(text="Не ниже", callback_data="alert_condition:>=")],
    ])
