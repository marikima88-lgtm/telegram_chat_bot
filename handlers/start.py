import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import save_or_update_user, set_user_language
from i18n import normalize_language, t
from keyboards.main import get_branch_keyboard, get_city_keyboard, get_language_keyboard, get_main_menu_keyboard
from services.branches import get_branch_display, get_branch_info, get_city_name

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
    await message.answer(t("choose_language"), reply_markup=get_language_keyboard("lang_start"))


@router.callback_query(F.data.startswith("lang_start:"))
async def select_start_language(callback: CallbackQuery) -> None:
    lang = normalize_language(callback.data.split(":", 1)[1])
    await set_user_language(callback.from_user.id, lang)
    await callback.message.edit_text(t("welcome", lang), reply_markup=get_city_keyboard(lang))


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await callback.message.edit_text(
        t("choose_language", lang),
        reply_markup=get_language_keyboard("set_lang", with_back=True, lang=lang),
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(callback: CallbackQuery) -> None:
    lang = normalize_language(callback.data.split(":", 1)[1])
    await set_user_language(callback.from_user.id, lang)
    await callback.message.edit_text(t("main_menu", lang), reply_markup=get_main_menu_keyboard(lang))


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await message.answer(t("cancelled", lang), reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data == "main_menu")
async def go_main_menu(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await callback.message.edit_text(t("main_menu", lang), reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data == "change_branch")
async def change_branch(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await callback.message.edit_text(t("choose_city", lang), reply_markup=get_city_keyboard(lang))


@router.callback_query(F.data.startswith("city:"))
async def select_city(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    city_id = callback.data.split(":", 1)[1]
    await state.update_data(city_id=city_id)
    await callback.message.edit_text(t("choose_branch", lang), reply_markup=get_branch_keyboard(city_id, lang))


@router.callback_query(F.data.startswith("branch:"))
async def select_branch(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
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
    branch_name = get_branch_display(branch_id, lang) if get_branch_info(branch_id) else branch_id
    city_name = get_city_name(city_id, lang)
    await callback.message.edit_text(
        t("branch_selected", lang, city=city_name or t("not_specified", lang), branch=branch_name),
        reply_markup=get_main_menu_keyboard(lang),
    )
