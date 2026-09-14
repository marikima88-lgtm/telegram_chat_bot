from decimal import Decimal

from aiogram import F, Router
from aiogram.types import CallbackQuery

from database import get_user
from i18n import t
from keyboards.common import get_back_keyboard
from keyboards.rates import get_all_currencies_keyboard, get_dynamic_rates_menu_keyboard, get_rate_detail_keyboard
from services.branches import get_branch_display
from services.currency_display import get_currency_flag, get_currency_label, sort_currency_codes
from services.rate_provider import RateProvider

router = Router()

MAIN_CURRENCY_CODES = ["USD", "EUR", "RUB", "GOLD1"]


@router.callback_query(F.data == "rates")
async def show_rates_menu(callback: CallbackQuery, lang: str) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer(t("select_branch_first", lang))
        return

    provider = RateProvider()
    rates = await provider.get_all_rates(branch_id)
    if not rates:
        await callback.message.edit_text(t("rates_unavailable_menu", lang), reply_markup=get_back_keyboard(lang))
        return

    main_codes = [code for code in MAIN_CURRENCY_CODES if code in rates]
    await callback.message.edit_text(
        t("rates_menu", lang, branch=get_branch_display(branch_id, lang)),
        reply_markup=get_dynamic_rates_menu_keyboard(main_codes, lang),
    )


@router.callback_query(F.data.startswith("rate_currency:"))
async def show_currency_rate(callback: CallbackQuery, lang: str) -> None:
    currency_code = callback.data.split(":", 1)[1]
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer(t("select_branch_first", lang))
        return

    provider = RateProvider()
    rate = await provider.get_rate(branch_id, currency_code)
    if not rate:
        await callback.message.edit_text(t("rate_unavailable", lang), reply_markup=get_rate_detail_keyboard(lang))
        return

    text = t(
        "rate_detail",
        lang,
        flag=get_currency_flag(currency_code),
        label=get_currency_label(currency_code, lang),
        branch=get_branch_display(branch_id, lang),
        buy=Decimal(str(rate["buy"])),
        sell=Decimal(str(rate["sell"])),
    )
    await callback.message.edit_text(text, reply_markup=get_rate_detail_keyboard(lang))


@router.callback_query(F.data == "all_rates")
async def show_all_rates(callback: CallbackQuery, lang: str) -> None:
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    if not branch_id:
        await callback.answer(t("select_branch_first", lang))
        return

    provider = RateProvider()
    rates = await provider.get_all_rates(branch_id)
    if not rates:
        await callback.message.edit_text(t("rates_unavailable", lang), reply_markup=get_rate_detail_keyboard(lang))
        return

    codes = sort_currency_codes(rates.keys())
    lines = [t("branch_line", lang, branch=get_branch_display(branch_id, lang)), "", t("buy_sell_header", lang), ""]
    for code in codes:
        rate = rates[code]
        buy = Decimal(str(rate["buy"]))
        sell = Decimal(str(rate["sell"]))
        lines.append(f"{get_currency_flag(code)} {get_currency_label(code, lang)} {buy} | {sell}")
    lines += ["", t("choose_currency_detail", lang)]
    await callback.message.edit_text("\n".join(lines), reply_markup=get_all_currencies_keyboard(codes, lang))
