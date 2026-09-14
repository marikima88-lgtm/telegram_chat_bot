from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import DEFAULT_LANGUAGE, t

FAQ_TOPIC_IDS = ["rate", "address", "cashless", "exchange", "crypto"]


def get_faq_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t(f"faq_q_{topic_id}", lang), callback_data=f"faq_topic:{topic_id}")]
        for topic_id in FAQ_TOPIC_IDS
    ]
    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_faq_answer_keyboard(lang: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_to_questions", lang), callback_data="faq")],
            [InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu")],
        ]
    )
