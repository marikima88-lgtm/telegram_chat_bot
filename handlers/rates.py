import json
from decimal import Decimal
from typing import Any

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.rates import get_dynamic_rates_menu_keyboard, get_rates_menu_keyboard
from services.branches import get_branch_display
from services.rate_provider import RateProvider
from database import get_user

router = Router()


@router.callback_query(F.data == "rates")
async def show_rates_menu(callback: CallbackQuery) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer("Сначала выберите филиал в меню.")
        return

    provider = RateProvider()
    rates = await provider.get_all_rates(branch_id)
    currency_codes = sorted(rates.keys())
    
    if not currency_codes:
        await callback.message.edit_text(
            "📊 Курсы валют\n\n"
            "Курсы для выбранного филиала пока не доступны. "
            "Попробуйте позже."
        )
        return
    
    branch_name = get_branch_display(branch_id)
    await callback.message.edit_text(
        f"💱 Курсы валют\n"
        f"Филиал: {branch_name}\n\n"
        f"Доступные валюты: {', '.join(currency_codes)}\n\n"
        f"Выберите валюту для подробной информации:",
        reply_markup=get_dynamic_rates_menu_keyboard(currency_codes)
    )


@router.callback_query(F.data.startswith("rate_currency:"))
async def show_currency_rate(callback: CallbackQuery) -> None:
    currency_code = callback.data.split(":", 1)[1]
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer("Сначала выберите филиал.")
        return

    provider = RateProvider()
    rate = await provider.get_rate(branch_id, currency_code)
    if not rate:
        await callback.message.edit_text("Курс для этой валюты пока не доступен.")
        return

    branch_name = get_branch_display(branch_id)

    source_note = "Актуальные данные из Quiq" if rate.get("source") == "api" else "Демонстрационные данные"
    text = (
        f"💱 {currency_code}\n\n"
        f"Филиал: {branch_name}\n\n"
        f"💵 Покупка: {Decimal(str(rate['buy'])).quantize(Decimal('1'))} ₸\n"
        f"💴 Продажа: {Decimal(str(rate['sell'])).quantize(Decimal('1'))} ₸\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', '—')}\n"
        f"{source_note}"
    )
    await callback.message.edit_text(text)


@router.callback_query(F.data == "all_rates")
async def show_all_rates(callback: CallbackQuery) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer("Сначала выберите филиал.")
        return

    provider = RateProvider()
    rates = await provider.get_all_rates(branch_id)
    if not rates:
        await callback.message.edit_text("Курсы для выбранного филиала пока не доступны.")
        return

    branch_name = get_branch_display(branch_id)

    lines = [f"Филиал: {branch_name}", "", "Все доступные валюты", ""]
    for code, rate in rates.items():
        lines.append(
            f"{code}: покупка {Decimal(str(rate['buy'])).quantize(Decimal('1'))} ₸, продажа {Decimal(str(rate['sell'])).quantize(Decimal('1'))} ₸"
        )
    await callback.message.edit_text("\n".join(lines))
