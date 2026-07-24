import json
from decimal import Decimal
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_CHAT_ID
from database import get_user, save_application
from keyboards.common import get_back_keyboard, get_main_menu_keyboard
from keyboards.services import get_booking_keyboard, get_individual_rate_keyboard
from states import MainStates

router = Router()


@router.callback_query(F.data == "booking")
async def start_booking(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainStates.booking_operation)
    await callback.message.edit_text(
        "📝 Бронирование валюты\n\n"
        "Какая операция вам нужна?\n",
        reply_markup=get_booking_keyboard(),
    )


@router.callback_query(F.data == "individual_rate")
async def start_individual_rate(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainStates.rate_request_operation)
    await callback.message.edit_text(
        "⭐ Запрос индивидуального курса\n\n"
        "Наши специалисты рассмотрят ваш запрос и ответят через переговоры.\n\n"
        "Какая операция вам нужна?\n",
        reply_markup=get_individual_rate_keyboard(),
    )


@router.callback_query(F.data.startswith("booking_op:"))
async def booking_operation(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(booking_operation=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.booking_currency)
    await callback.message.edit_text("Выберите валюту:", reply_markup=get_booking_keyboard("currency"))


@router.callback_query(F.data.startswith("rate_req_op:"))
async def rate_request_operation(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(rate_request_operation=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.rate_request_currency)
    await callback.message.edit_text("Выберите валюту:", reply_markup=get_individual_rate_keyboard("currency"))


@router.callback_query(F.data.startswith("booking_currency:"))
async def booking_currency(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(booking_currency=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.booking_amount)
    await callback.message.edit_text(
        "💵 Какую сумму в иностранной валюте хотите забронировать?\n\n"
        "Напишите цифру:"
    )


@router.callback_query(F.data.startswith("rate_req_currency:"))
async def rate_request_currency(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(rate_request_currency=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.rate_request_amount)
    await callback.message.edit_text(
        "💵 Какая сумма вам нужна?\n\n"
        "Напишите цифру:"
    )


@router.message(MainStates.booking_amount)
async def booking_amount(message: Message, state: FSMContext) -> None:
    try:
        Decimal(message.text)
    except Exception:
        await message.answer("Пожалуйста, введите корректную сумму.")
        return
    await state.update_data(booking_amount=message.text)
    await state.set_state(MainStates.booking_nominals)
    await message.answer("Нужны ли определённые номиналы?", reply_markup=get_booking_keyboard("nominals"))


@router.message(MainStates.rate_request_amount)
async def rate_request_amount(message: Message, state: FSMContext) -> None:
    try:
        Decimal(message.text)
    except Exception:
        await message.answer("Пожалуйста, введите корректную сумму.")
        return
    await state.update_data(rate_request_amount=message.text)
    await state.set_state(MainStates.rate_request_name)
    await message.answer("Введите ваше имя:")


@router.message(MainStates.booking_nominals)
async def booking_nominals(message: Message, state: FSMContext) -> None:
    await state.update_data(booking_nominals=message.text)
    await state.set_state(MainStates.booking_name)
    await message.answer("Введите ваше имя:")


@router.message(MainStates.booking_name)
async def booking_name(message: Message, state: FSMContext) -> None:
    await state.update_data(booking_name=message.text)
    await state.set_state(MainStates.booking_phone)
    await message.answer("Введите номер телефона или отправьте контакт:")


@router.message(MainStates.rate_request_name)
async def rate_request_name(message: Message, state: FSMContext) -> None:
    await state.update_data(rate_request_name=message.text)
    await state.set_state(MainStates.rate_request_phone)
    await message.answer("Введите номер телефона или отправьте контакт:")


@router.message(MainStates.booking_phone)
async def booking_phone(message: Message, state: FSMContext) -> None:
    phone = message.text or ""
    if message.contact:
        phone = message.contact.phone_number
    if not phone:
        await message.answer("Пожалуйста, введите номер телефона или отправьте контакт.")
        return
    await state.update_data(booking_phone=phone)
    await state.set_state(MainStates.booking_comment)
    await message.answer("Оставьте комментарий, если нужно:")


@router.message(MainStates.rate_request_phone)
async def rate_request_phone(message: Message, state: FSMContext) -> None:
    phone = message.text or ""
    if message.contact:
        phone = message.contact.phone_number
    if not phone:
        await message.answer("Пожалуйста, введите номер телефона или отправьте контакт.")
        return
    await state.update_data(rate_request_phone=phone)
    await state.set_state(MainStates.rate_request_comment)
    await message.answer("Оставьте комментарий, если нужно:")


@router.message(MainStates.booking_comment)
async def booking_comment(message: Message, state: FSMContext) -> None:
    await state.update_data(booking_comment=message.text)
    data = await state.get_data()
    text = (
        "Проверьте заявку:\n\n"
        f"Операция: {data.get('booking_operation')}\n"
        f"Валюта: {data.get('booking_currency')}\n"
        f"Сумма: {data.get('booking_amount')}\n"
        f"Желаемые номиналы: {data.get('booking_nominals')}\n"
        f"Имя: {data.get('booking_name')}\n"
        f"Телефон: {data.get('booking_phone')}\n"
        f"Комментарий: {data.get('booking_comment')}"
    )
    await state.set_state(MainStates.booking_review)
    await message.answer(text, reply_markup=get_booking_keyboard("review"))


@router.message(MainStates.rate_request_comment)
async def rate_request_comment(message: Message, state: FSMContext) -> None:
    await state.update_data(rate_request_comment=message.text)
    data = await state.get_data()
    text = (
        "Проверьте заявку:\n\n"
        f"Операция: {data.get('rate_request_operation')}\n"
        f"Валюта: {data.get('rate_request_currency')}\n"
        f"Сумма: {data.get('rate_request_amount')}\n"
        f"Имя: {data.get('rate_request_name')}\n"
        f"Телефон: {data.get('rate_request_phone')}\n"
        f"Комментарий: {data.get('rate_request_comment')}"
    )
    await state.set_state(MainStates.rate_request_review)
    await message.answer(text, reply_markup=get_individual_rate_keyboard("review"))


@router.callback_query(F.data == "confirm_booking")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    request_text = (
        "📥 Новое бронирование Ecash\n\n"
        f"Город: {user.get('city_id') if user else '-'}\n"
        f"Филиал: {branch_id or '-'}\n"
        f"Операция: {data.get('booking_operation')}\n"
        f"Валюта: {data.get('booking_currency')}\n"
        f"Сумма: {data.get('booking_amount')}\n"
        f"Желаемые номиналы: {data.get('booking_nominals')}\n"
        f"Имя: {data.get('booking_name')}\n"
        f"Телефон: {data.get('booking_phone')}\n"
        f"Комментарий: {data.get('booking_comment')}\n"
        f"Telegram username: {callback.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {callback.from_user.id}\n"
        f"Дата и время заявки: {datetime.utcnow().isoformat()}"
    )
    try:
        await callback.message.answer("Спасибо! Заявка на бронирование передана сотруднику Ecash.")
        if ADMIN_CHAT_ID:
            await callback.bot.send_message(ADMIN_CHAT_ID, request_text)
    except Exception as exc:
        await callback.message.answer(f"Не удалось отправить заявку: {exc}")
    await save_application(callback.from_user.id, "booking", branch_id, data)
    await state.clear()
    await callback.message.answer("Бронирование считается подтверждённым только после ответа сотрудника.", reply_markup=get_main_menu_keyboard())


@router.callback_query(F.data == "confirm_individual")
async def confirm_individual(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    request_text = (
        "⭐ Запрос на индивидуальный курс\n\n"
        f"Город: {user.get('city_id') if user else '-'}\n"
        f"Филиал: {branch_id or '-'}\n"
        f"Операция: {data.get('rate_request_operation')}\n"
        f"Валюта: {data.get('rate_request_currency')}\n"
        f"Сумма: {data.get('rate_request_amount')}\n"
        f"Желаемый курс: {data.get('rate_request_preference', '-')}\n"
        f"Желаемые номиналы: {data.get('rate_request_nominals', '-')}\n"
        f"Имя: {data.get('rate_request_name')}\n"
        f"Телефон: {data.get('rate_request_phone')}\n"
        f"Комментарий: {data.get('rate_request_comment')}\n"
        f"Telegram username: {callback.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {callback.from_user.id}\n"
        f"Дата и время заявки: {datetime.utcnow().isoformat()}"
    )
    try:
        await callback.message.answer("Спасибо! Запрос на индивидуальный курс передан казначею Ecash.")
        if ADMIN_CHAT_ID:
            await callback.bot.send_message(ADMIN_CHAT_ID, request_text)
    except Exception as exc:
        await callback.message.answer(f"Не удалось отправить заявку: {exc}")
    await save_application(callback.from_user.id, "individual_rate", branch_id, data)
    await state.clear()
    await callback.message.answer("Индивидуальный курс не гарантирован и определяется сотрудником с учётом валюты, суммы и текущей ситуации на рынке.", reply_markup=get_main_menu_keyboard())
