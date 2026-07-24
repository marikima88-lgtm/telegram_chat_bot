from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.branches import load_branches


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="💱 Курсы валют", callback_data="rates"), InlineKeyboardButton(text="📍 Адрес & График", callback_data="contacts")],
        [InlineKeyboardButton(text="📝 Забронировать", callback_data="booking"), InlineKeyboardButton(text="⭐ Инд. курс", callback_data="individual_rate")],
        [InlineKeyboardButton(text="🔔 Оповещение", callback_data="alerts"), InlineKeyboardButton(text="❓ Вопросы", callback_data="faq")],
        [InlineKeyboardButton(text="📞 Связь с казначеем", callback_data="contacts")],
        [InlineKeyboardButton(text="🏙 Сменить филиал", callback_data="change_branch")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_city_keyboard() -> InlineKeyboardMarkup:
    data = load_branches()
    buttons = [[InlineKeyboardButton(text=city_info.get("name", city_id), callback_data=f"city:{city_id}")] for city_id, city_info in data.items()]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_branch_keyboard(city_id: str) -> InlineKeyboardMarkup:
    data = load_branches()
    city_data = data.get(city_id, {})
    buttons = []
    for branch_id, branch_info in city_data.get("branches", {}).items():
        buttons.append([InlineKeyboardButton(text=branch_info["name"], callback_data=f"branch:{branch_id}")])
    if not buttons:
        buttons.append([InlineKeyboardButton(text="Нет доступных филиалов", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
