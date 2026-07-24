from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import json

from config import ADMIN_CHAT_ID
from database import get_user, save_application
from keyboards.common import get_main_menu_keyboard
from keyboards.contacts import get_contacts_keyboard
from services.branches import get_branch_info, get_branch_location
from states import MainStates

router = Router()


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    branch_info = get_branch_info(branch_id)

    if branch_info:
        address, landmark, schedule, map_url = get_branch_location(branch_id)
        text = (
            f"📍 {branch_info.get('name', 'Филиал')}\n\n"
            f"📮 Адрес:\n{address or '-'}\n\n"
            f"🧭 Ориентир:\n{landmark or '-'}\n\n"
            f"🕐 График:\n{schedule or '-'}\n\n"
            f"💡 Откройте в 2GIS, чтобы найти маршрут до нас."
        )
        await callback.message.edit_text(text, reply_markup=get_contacts_keyboard(map_url))
    else:
        await callback.message.edit_text(
            "📍 Адреса и график\n\n"
            "Сначала выберите филиал, чтобы увидеть информацию о нём.\n\n"
            "Откройте меню и нажмите 'Сменить филиал'.",
            reply_markup=get_contacts_keyboard()
        )


@router.callback_query(F.data == "call_back")
async def start_callback_request(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainStates.callback_name)
    await callback.message.edit_text("Введите ваше имя:")


@router.message(MainStates.callback_name)
async def callback_name(message: Message, state: FSMContext) -> None:
    await state.update_data(callback_name=message.text)
    await state.set_state(MainStates.callback_phone)
    await message.answer("Введите номер телефона:")


@router.message(MainStates.callback_phone)
async def callback_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(callback_phone=message.text)
    await state.set_state(MainStates.callback_theme)
    await message.answer("Введите тему обращения:")


@router.message(MainStates.callback_theme)
async def callback_theme(message: Message, state: FSMContext) -> None:
    await state.update_data(callback_theme=message.text)
    await state.set_state(MainStates.callback_comment)
    await message.answer("Оставьте комментарий:")


@router.message(MainStates.callback_comment)
async def callback_comment(message: Message, state: FSMContext) -> None:
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
        f"Telegram username: {message.from_user.username or 'Не указан'}\n"
        f"Telegram ID: {message.from_user.id}"
    )
    if ADMIN_CHAT_ID:
        await message.bot.send_message(ADMIN_CHAT_ID, request_text)
    await save_application(message.from_user.id, "callback", branch_id, data)
    await state.clear()
    await message.answer("Заявка передана сотруднику.", reply_markup=get_main_menu_keyboard())
