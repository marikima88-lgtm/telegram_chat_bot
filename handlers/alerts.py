from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import add_rate_alert, deactivate_all_alerts, get_user, list_rate_alerts
from i18n import t
from keyboards.alerts import get_alert_condition_keyboard, get_alert_currency_keyboard, get_alert_keyboard, get_alert_rate_type_keyboard
from keyboards.common import get_back_keyboard, get_main_menu_keyboard
from states import MainStates

router = Router()

RATE_TYPE_KEYS = {"buy": "rate_type_buy", "sell": "rate_type_sell"}
CONDITION_KEYS = {"<=": "condition_le", ">=": "condition_ge"}


def _label(value: str | None, keys: dict[str, str], lang: str) -> str:
    key = keys.get(value or "")
    return t(key, lang) if key else (value or "-")


@router.callback_query(F.data == "alerts")
async def open_alerts(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    alerts = await list_rate_alerts(callback.from_user.id)
    if not alerts:
        await callback.message.edit_text(t("no_alerts", lang), reply_markup=get_alert_keyboard(lang=lang))
        return
    lines = [t("alerts_list", lang)]
    for alert in alerts:
        rate_type = _label(alert["rate_type"], RATE_TYPE_KEYS, lang)
        condition = _label(alert["condition_type"], CONDITION_KEYS, lang)
        lines.append(f"- {alert['currency_code']} / {rate_type} / {condition} / {alert['target_rate']}")
    await callback.message.edit_text("\n".join(lines), reply_markup=get_alert_keyboard(lang=lang))


@router.callback_query(F.data == "create_alert")
async def create_alert(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.set_state(MainStates.alert_currency)
    await callback.message.edit_text(t("choose_currency", lang), reply_markup=get_alert_currency_keyboard(lang))


@router.callback_query(F.data.startswith("alert_currency:"))
async def alert_currency(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(alert_currency=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_rate_type)
    await callback.message.edit_text(t("choose_rate_type", lang), reply_markup=get_alert_rate_type_keyboard(lang))


@router.callback_query(F.data.startswith("alert_rate_type:"))
async def alert_rate_type(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(alert_rate_type=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_condition)
    await callback.message.edit_text(t("choose_condition", lang), reply_markup=get_alert_condition_keyboard(lang))


@router.callback_query(F.data.startswith("alert_condition:"))
async def alert_condition(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(alert_condition=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_target_rate)
    await callback.message.edit_text(t("enter_target_rate", lang), reply_markup=get_back_keyboard(lang))


@router.message(MainStates.alert_target_rate)
async def alert_target_rate(message: Message, state: FSMContext, lang: str) -> None:
    await state.update_data(alert_target_rate=message.text)
    data = await state.get_data()
    text = (
        f"{t('review_alert', lang)}\n\n"
        f"{t('field_currency', lang)}: {data.get('alert_currency')}\n"
        f"{t('field_rate_type', lang)}: {_label(data.get('alert_rate_type'), RATE_TYPE_KEYS, lang)}\n"
        f"{t('field_condition', lang)}: {_label(data.get('alert_condition'), CONDITION_KEYS, lang)}\n"
        f"{t('field_target_rate', lang)}: {data.get('alert_target_rate')}"
    )
    await state.set_state(MainStates.alert_confirmation)
    await message.answer(text, reply_markup=get_alert_keyboard("confirm", lang))


@router.callback_query(F.data == "confirm_alert")
async def confirm_alert(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    await add_rate_alert(callback.from_user.id, branch_id or "", data.get("alert_currency"), data.get("alert_rate_type"), data.get("alert_condition"), data.get("alert_target_rate"))
    await callback.message.answer(t("alert_saved", lang), reply_markup=get_main_menu_keyboard(lang))
    await state.clear()


@router.callback_query(F.data == "delete_all_alerts")
async def delete_all_alerts(callback: CallbackQuery, lang: str) -> None:
    await deactivate_all_alerts(callback.from_user.id)
    await callback.message.edit_text(t("alerts_disabled", lang), reply_markup=get_main_menu_keyboard(lang))
