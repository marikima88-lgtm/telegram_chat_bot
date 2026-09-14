from decimal import Decimal
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_CHAT_ID
from database import get_user, save_application
from i18n import LANGUAGES, t
from keyboards.common import get_back_keyboard, get_main_menu_keyboard
from keyboards.services import get_booking_keyboard, get_currency_picker_keyboard, get_individual_rate_keyboard
from services.phone import PHONE_MASK_EXAMPLE, normalize_phone
from states import MainStates

router = Router()

# Заявки для сотрудников всегда на русском, независимо от языка клиента.
ADMIN_LANGUAGE = "ru"


def _operation_label(operation: str | None, lang: str) -> str:
    if operation in ("buy", "sell"):
        return t(f"op_{operation}", lang)
    return operation or "-"


def _nominals_label(nominals: str | None, lang: str) -> str:
    return nominals or t("no", lang)


@router.callback_query(F.data == "booking")
async def start_booking(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.set_state(MainStates.booking_operation)
    await callback.message.edit_text(t("booking_start", lang), reply_markup=get_booking_keyboard(lang=lang))


@router.callback_query(F.data == "individual_rate")
async def start_individual_rate(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.set_state(MainStates.rate_request_operation)
    await callback.message.edit_text(t("individual_start", lang), reply_markup=get_individual_rate_keyboard(lang=lang))


@router.callback_query(F.data.startswith("booking_op:"))
async def booking_operation(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(booking_operation=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.booking_currency)
    await callback.message.edit_text(t("choose_currency", lang), reply_markup=get_booking_keyboard("currency", lang))


@router.callback_query(F.data.startswith("rate_req_op:"))
async def rate_request_operation(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(rate_request_operation=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.rate_request_currency)
    await callback.message.edit_text(t("choose_currency", lang), reply_markup=get_individual_rate_keyboard("currency", lang))


@router.callback_query(F.data.startswith("booking_currency:"))
async def booking_currency(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    currency = callback.data.split(":", 1)[1]
    if currency == "OTHER":
        await callback.message.edit_text(
            t("choose_currency", lang),
            reply_markup=get_currency_picker_keyboard("booking_currency", lang),
        )
        return
    await state.update_data(booking_currency=currency)
    await state.set_state(MainStates.booking_amount)
    await callback.message.edit_text(t("enter_amount", lang), reply_markup=get_back_keyboard(lang))


@router.callback_query(F.data.startswith("rate_req_currency:"))
async def rate_request_currency(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    currency = callback.data.split(":", 1)[1]
    if currency == "OTHER":
        await callback.message.edit_text(
            t("choose_currency", lang),
            reply_markup=get_currency_picker_keyboard("rate_req_currency", lang),
        )
        return
    await state.update_data(rate_request_currency=currency)
    await state.set_state(MainStates.rate_request_amount)
    await callback.message.edit_text(t("enter_amount", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.booking_amount)
async def booking_amount(message: Message, state: FSMContext, lang: str) -> None:
    try:
        Decimal(message.text)
    except Exception:
        await message.answer(t("invalid_amount", lang), reply_markup=get_back_keyboard(lang))
        return
    await state.update_data(booking_amount=message.text)
    await state.set_state(MainStates.booking_nominals)
    await message.answer(t("need_nominals", lang), reply_markup=get_booking_keyboard("nominals", lang))


@router.message(MainStates.rate_request_amount)
async def rate_request_amount(message: Message, state: FSMContext, lang: str) -> None:
    try:
        Decimal(message.text)
    except Exception:
        await message.answer(t("invalid_amount", lang), reply_markup=get_back_keyboard(lang))
        return
    await state.update_data(rate_request_amount=message.text)
    await state.set_state(MainStates.rate_request_name)
    await message.answer(t("enter_name", lang), reply_markup=get_back_keyboard(lang))


@router.callback_query(F.data.startswith("booking_nominals:"))
async def booking_nominals_choice(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    choice = callback.data.split(":", 1)[1]
    if choice == "no":
        await state.update_data(booking_nominals=None)
        await state.set_state(MainStates.booking_name)
        await callback.message.edit_text(t("enter_name", lang), reply_markup=get_back_keyboard(lang))
        return
    await callback.message.edit_text(t("enter_nominals", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.booking_nominals)
async def booking_nominals(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(booking_nominals=message.text)
    await state.set_state(MainStates.booking_name)
    await message.answer(t("enter_name", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.booking_name)
async def booking_name(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(booking_name=message.text)
    await state.set_state(MainStates.booking_phone)
    await message.answer(t("enter_phone_or_contact", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.rate_request_name)
async def rate_request_name(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(rate_request_name=message.text)
    await state.set_state(MainStates.rate_request_phone)
    await message.answer(t("enter_phone_or_contact", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.booking_phone)
async def booking_phone(message: Message, state: FSMContext, lang: str) -> None:
    raw_phone = message.contact.phone_number if message.contact else (message.text or "")
    phone = normalize_phone(raw_phone)
    if not phone:
        await message.answer(t("invalid_phone_or_contact", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))
        return
    await state.update_data(booking_phone=phone)
    await state.set_state(MainStates.booking_comment)
    await message.answer(t("enter_comment_optional", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.rate_request_phone)
async def rate_request_phone(message: Message, state: FSMContext, lang: str) -> None:
    raw_phone = message.contact.phone_number if message.contact else (message.text or "")
    phone = normalize_phone(raw_phone)
    if not phone:
        await message.answer(t("invalid_phone_or_contact", lang, mask=PHONE_MASK_EXAMPLE), reply_markup=get_back_keyboard(lang))
        return
    await state.update_data(rate_request_phone=phone)
    await state.set_state(MainStates.rate_request_comment)
    await message.answer(t("enter_comment_optional", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.booking_comment)
async def booking_comment(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(booking_comment=message.text)
    data = await state.get_data()
    text = (
        f"{t('review_request', lang)}\n\n"
        f"{t('field_operation', lang)}: {_operation_label(data.get('booking_operation'), lang)}\n"
        f"{t('field_currency', lang)}: {data.get('booking_currency')}\n"
        f"{t('field_amount', lang)}: {data.get('booking_amount')}\n"
        f"{t('field_nominals', lang)}: {_nominals_label(data.get('booking_nominals'), lang)}\n"
        f"{t('field_name', lang)}: {data.get('booking_name')}\n"
        f"{t('field_phone', lang)}: {data.get('booking_phone')}\n"
        f"{t('field_comment', lang)}: {data.get('booking_comment')}"
    )
    await state.set_state(MainStates.booking_review)
    await message.answer(text, reply_markup=get_booking_keyboard("review", lang))


@router.message(MainStates.rate_request_comment)
async def rate_request_comment(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(rate_request_comment=message.text)
    data = await state.get_data()
    text = (
        f"{t('review_request', lang)}\n\n"
        f"{t('field_operation', lang)}: {_operation_label(data.get('rate_request_operation'), lang)}\n"
        f"{t('field_currency', lang)}: {data.get('rate_request_currency')}\n"
        f"{t('field_amount', lang)}: {data.get('rate_request_amount')}\n"
        f"{t('field_name', lang)}: {data.get('rate_request_name')}\n"
        f"{t('field_phone', lang)}: {data.get('rate_request_phone')}\n"
        f"{t('field_comment', lang)}: {data.get('rate_request_comment')}"
    )
    await state.set_state(MainStates.rate_request_review)
    await message.answer(text, reply_markup=get_individual_rate_keyboard("review", lang))


@router.callback_query(F.data == "confirm_booking")
async def confirm_booking(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    request_text = (
        "📥 Новое бронирование Ecash\n\n"
        f"Город: {user.get('city_id') if user else '-'}\n"
        f"Филиал: {branch_id or '-'}\n"
        f"Операция: {_operation_label(data.get('booking_operation'), ADMIN_LANGUAGE)}\n"
        f"Валюта: {data.get('booking_currency')}\n"
        f"Сумма: {data.get('booking_amount')}\n"
        f"Желаемые номиналы: {_nominals_label(data.get('booking_nominals'), ADMIN_LANGUAGE)}\n"
        f"Имя: {data.get('booking_name')}\n"
        f"Телефон: {data.get('booking_phone')}\n"
        f"Комментарий: {data.get('booking_comment')}\n"
        f"Язык клиента: {LANGUAGES[lang]}\n"
        f"Telegram username: {callback.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {callback.from_user.id}\n"
        f"Дата и время заявки: {datetime.utcnow().isoformat()}"
    )
    try:
        await callback.message.answer(t("booking_sent", lang))
        if ADMIN_CHAT_ID:
            await callback.bot.send_message(ADMIN_CHAT_ID, request_text)
    except Exception as exc:
        await callback.message.answer(t("send_failed", lang, error=exc))
    await save_application(callback.from_user.id, "booking", branch_id, data)
    await state.clear()
    await callback.message.answer(t("booking_note", lang), reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data == "confirm_individual")
async def confirm_individual(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    request_text = (
        "⭐ Запрос на индивидуальный курс\n\n"
        f"Город: {user.get('city_id') if user else '-'}\n"
        f"Филиал: {branch_id or '-'}\n"
        f"Операция: {_operation_label(data.get('rate_request_operation'), ADMIN_LANGUAGE)}\n"
        f"Валюта: {data.get('rate_request_currency')}\n"
        f"Сумма: {data.get('rate_request_amount')}\n"
        f"Желаемый курс: {data.get('rate_request_preference', '-')}\n"
        f"Желаемые номиналы: {data.get('rate_request_nominals', '-')}\n"
        f"Имя: {data.get('rate_request_name')}\n"
        f"Телефон: {data.get('rate_request_phone')}\n"
        f"Комментарий: {data.get('rate_request_comment')}\n"
        f"Язык клиента: {LANGUAGES[lang]}\n"
        f"Telegram username: {callback.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {callback.from_user.id}\n"
        f"Дата и время заявки: {datetime.utcnow().isoformat()}"
    )
    try:
        await callback.message.answer(t("individual_sent", lang))
        if ADMIN_CHAT_ID:
            await callback.bot.send_message(ADMIN_CHAT_ID, request_text)
    except Exception as exc:
        await callback.message.answer(t("send_failed", lang, error=exc))
    await save_application(callback.from_user.id, "individual_rate", branch_id, data)
    await state.clear()
    await callback.message.answer(t("individual_note", lang), reply_markup=get_main_menu_keyboard(lang))
