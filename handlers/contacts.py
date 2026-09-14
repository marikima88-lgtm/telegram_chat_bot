from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_CHAT_ID
from database import get_user, save_application
from i18n import LANGUAGES, t
from keyboards.common import get_back_keyboard, get_main_menu_keyboard
from keyboards.contacts import get_contacts_keyboard
from services.branches import get_branch_info, get_branch_location
from services.phone import PHONE_MASK_EXAMPLE, normalize_phone
from states import MainStates

router = Router()

TREASURER_PHONE = "+77003332223"


@router.callback_query(F.data == "treasurer_contact")
async def show_treasurer_contact(callback: CallbackQuery, lang: str) -> None:
    await callback.message.edit_text(t("treasurer", lang, phone=TREASURER_PHONE), reply_markup=get_contacts_keyboard(lang=lang))
    await callback.message.answer_contact(phone_number=TREASURER_PHONE, first_name=t("treasurer_contact_name", lang))


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery, lang: str) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    branch_info = get_branch_info(branch_id)

    if branch_info:
        address, landmark, schedule, map_url = get_branch_location(branch_id)
        text = t(
            "branch_card",
            lang,
            name=branch_info.get("name") or t("branch_default_name", lang),
            address=address or "-",
            landmark=landmark or "-",
            schedule=schedule or "-",
        )
        await callback.message.edit_text(text, reply_markup=get_contacts_keyboard(map_url, lang))
    else:
        await callback.message.edit_text(t("contacts_no_branch", lang), reply_markup=get_contacts_keyboard(lang=lang))


@router.callback_query(F.data == "call_back")
async def start_callback_request(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.set_state(MainStates.callback_name)
    await callback.message.edit_text(t("enter_name", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.callback_name)
async def callback_name(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(callback_name=message.text)
    await state.set_state(MainStates.callback_phone)
    await message.answer(t("enter_phone", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.callback_phone)
async def callback_phone(message: Message, state: FSMContext, lang: str) -> None:
    raw_phone = message.contact.phone_number if message.contact else (message.text or "")
    phone = normalize_phone(raw_phone)
    if not phone:
        await message.answer(t("invalid_phone", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))
        return
    await state.update_data(callback_phone=phone)
    await state.set_state(MainStates.callback_theme)
    await message.answer(t("enter_theme", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.callback_theme)
async def callback_theme(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(callback_theme=message.text)
    await state.set_state(MainStates.callback_comment)
    await message.answer(t("enter_comment", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.callback_comment)
async def callback_comment(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(callback_comment=message.text)
    data = await state.get_data()
    user = await get_user(message.from_user.id)
    branch_id = user.get("branch_id") if user else None
    request_text = (
        "📞 Запрос на звонок\n\n"
        f"Город: {user.get('city_id') if user else '-'}\n"
        f"Филиал: {branch_id or '-'}\n"
        f"Имя: {data.get('callback_name')}\n"
        f"Телефон: {data.get('callback_phone')}\n"
        f"Тема: {data.get('callback_theme')}\n"
        f"Комментарий: {data.get('callback_comment')}\n"
        f"Язык клиента: {LANGUAGES[lang]}\n"
        f"Telegram username: {message.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {message.from_user.id}"
    )
    if ADMIN_CHAT_ID:
        await message.bot.send_message(ADMIN_CHAT_ID, request_text)
    await save_application(message.from_user.id, "callback", branch_id, data)
    await state.clear()
    await message.answer(t("callback_sent", lang), reply_markup=get_main_menu_keyboard(lang))
