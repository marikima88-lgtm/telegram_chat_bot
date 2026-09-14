from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, LANGUAGES, localize_city, t
from services.branches import load_branches


def get_language_keyboard(prefix: str, with_back: bool = False, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=title, callback_data=f"{prefix}:{code}")] for code, title in LANGUAGES.items()]
    if with_back:
        buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=t("btn_rates", lang), callback_data="rates"), InlineKeyboardButton(text=t("btn_contacts", lang), callback_data="contacts")],
        [InlineKeyboardButton(text=t("btn_booking", lang), callback_data="booking"), InlineKeyboardButton(text=t("btn_individual", lang), callback_data="individual_rate")],
        [InlineKeyboardButton(text=t("btn_alerts", lang), callback_data="alerts"), InlineKeyboardButton(text=t("btn_faq", lang), callback_data="faq")],
        [InlineKeyboardButton(text=t("btn_treasurer", lang), callback_data="treasurer_contact")],
        [InlineKeyboardButton(text=t("btn_change_branch", lang), callback_data="change_branch")],
        [InlineKeyboardButton(text=t("btn_language", lang), callback_data="change_language")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_city_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    data = load_branches()
    buttons = [
        [InlineKeyboardButton(text=localize_city(city_id, city_info.get("name", city_id), lang), callback_data=f"city:{city_id}")]
        for city_id, city_info in data.items()
    ]
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_branch_keyboard(city_id: str, lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    data = load_branches()
    city_data = data.get(city_id, {})
    buttons = []
    for branch_id, branch_info in city_data.get("branches", {}).items():
        buttons.append([InlineKeyboardButton(text=branch_info["name"], callback_data=f"branch:{branch_id}")])
    if not buttons:
        buttons.append([InlineKeyboardButton(text=t("no_branches", lang), callback_data="main_menu")])
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="change_branch")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
