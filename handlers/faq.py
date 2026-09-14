from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database import get_user
from i18n import t
from keyboards.common import get_main_menu_keyboard
from keyboards.faq import FAQ_TOPIC_IDS, get_faq_answer_keyboard, get_faq_keyboard
from services.branches import get_branch_display

router = Router()

FREE_TEXT_KEYWORDS = {
    "курс": "rate",
    "доллар": "rate",
    "usd": "rate",
    "eur": "rate",
    "rub": "rate",
    "бағам": "rate",
    "адрес": "address",
    "график": "address",
    "работаете": "address",
    "мекенжай": "address",
    "кесте": "address",
    "картой": "cashless",
    "kaspi": "cashless",
    "переводом": "cashless",
    "онлайн": "cashless",
    "картамен": "cashless",
    "аударым": "cashless",
    "размен": "exchange",
    "банкноты": "exchange",
    "ұсақта": "exchange",
    "usdt": "crypto",
    "крипт": "crypto",
}


async def _resolve_answer(topic_id: str, telegram_user_id: int, lang: str) -> str:
    if topic_id == "address":
        user = await get_user(telegram_user_id)
        branch_name = get_branch_display(user.get("branch_id") if user else None, lang)
        return t("faq_a_address", lang, branch_name=branch_name)
    return t(f"faq_a_{topic_id}", lang)


@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery, lang: str) -> None:
    await callback.message.edit_text(t("faq_title", lang), reply_markup=get_faq_keyboard(lang))


@router.callback_query(F.data.startswith("faq_topic:"))
async def show_faq_answer(callback: CallbackQuery, lang: str) -> None:
    topic_id = callback.data.split(":", 1)[1]
    if topic_id not in FAQ_TOPIC_IDS:
        await callback.answer(t("answer_not_found", lang))
        return
    answer = await _resolve_answer(topic_id, callback.from_user.id, lang)
    await callback.message.edit_text(answer, reply_markup=get_faq_answer_keyboard(lang))


@router.message()
async def handle_text(message: Message, lang: str) -> None:
    text = message.text.lower() if message.text else ""
    if not text:
        return
    for keyword, topic_id in FREE_TEXT_KEYWORDS.items():
        if keyword in text:
            answer = await _resolve_answer(topic_id, message.from_user.id, lang)
            await message.answer(answer, reply_markup=get_main_menu_keyboard(lang))
            return
    await message.answer(t("not_understood", lang), reply_markup=get_main_menu_keyboard(lang))
