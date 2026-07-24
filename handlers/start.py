import logging
from typing import Any

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_CHAT_ID
from database import get_user, save_or_update_user
from handlers import rates, services, alerts, contacts, faq
from keyboards.main import get_main_menu_keyboard, get_city_keyboard, get_branch_keyboard
from services.branches import get_branch_display, get_city_name
from services.rate_provider import RateProvider
from states import MainStates

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await save_or_update_user(
        telegram_user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        phone=None,
        city_id=None,
        branch_id=None,
    )

    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Я помогу вам быстро узнать курс, оформить заявку или найти нужный филиал Ecash.\n\n"
        "Что можно сделать здесь:\n"
        "• посмотреть актуальные курсы валют;\n"
        "• забронировать валюту;\n"
        "• запросить индивидуальный курс;\n"
        "• создать уведомление о нужном курсе;\n"
        "• узнать адрес и график работы;\n"
        "• связаться с казначеем.\n\n"
        "Сначала выберите город и филиал, чтобы информация была точной.",
        reply_markup=get_main_menu_keyboard(),
    )

    await message.answer(
        "📍 Выберите город, а затем филиал, чтобы мы показывали данные именно по вашему офису.",
        reply_markup=get_city_keyboard(),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Действие отменено. Возвращаемся в главное меню.", reply_markup=get_main_menu_keyboard())


@router.callback_query(F.data == "main_menu")
async def go_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Главное меню", reply_markup=get_main_menu_keyboard())


@router.callback_query(F.data == "change_branch")
async def change_branch(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("🏙 Выберите город, чтобы продолжить:", reply_markup=get_city_keyboard())


@router.callback_query(F.data.startswith("city:"))
async def select_city(callback: CallbackQuery, state: FSMContext) -> None:
    city_id = callback.data.split(":", 1)[1]
    await state.update_data(city_id=city_id)
    await callback.message.edit_text("🏢 Выберите филиал для этого города:", reply_markup=get_branch_keyboard(city_id))


@router.callback_query(F.data.startswith("branch:"))
async def select_branch(callback: CallbackQuery, state: FSMContext) -> None:
    branch_id = callback.data.split(":", 1)[1]
    data = await state.get_data()
    city_id = data.get("city_id")
    await save_or_update_user(
        telegram_user_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name,
        phone=None,
        city_id=city_id,
        branch_id=branch_id,
    )
    branch_name = get_branch_display(branch_id)
    city_name = get_city_name(city_id)
    await callback.message.edit_text(
        f"✅ Готово.\n\n"
        f"Город: {city_name or 'не указан'}\n"
        f"Филиал: {branch_name if branch_name != 'Не выбран' else branch_id}\n\n"
        f"Теперь можно продолжать и пользоваться сервисом.",
        reply_markup=get_main_menu_keyboard(),
    )
