from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import add_rate_alert, deactivate_all_alerts, deactivate_rate_alert, list_rate_alerts, get_user
from keyboards.alerts import get_alert_keyboard, get_alert_condition_keyboard, get_alert_currency_keyboard, get_alert_rate_type_keyboard
from keyboards.common import get_main_menu_keyboard
from states import MainStates

router = Router()


@router.callback_query(F.data == "alerts")
async def open_alerts(callback: CallbackQuery, state: FSMContext) -> None:
    alerts = await list_rate_alerts(callback.from_user.id)
    if not alerts:
        await callback.message.edit_text("У вас пока нет уведомлений.", reply_markup=get_alert_keyboard())
        return
    lines = ["Ваши активные уведомления:"]
    for alert in alerts:
        lines.append(f"- {alert['currency_code']} / {alert['rate_type']} / {alert['condition_type']} / {alert['target_rate']}")
    await callback.message.edit_text("\n".join(lines), reply_markup=get_alert_keyboard())


@router.callback_query(F.data == "create_alert")
async def create_alert(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainStates.alert_currency)
    await callback.message.edit_text("Выберите валюту:", reply_markup=get_alert_currency_keyboard())


@router.callback_query(F.data.startswith("alert_currency:"))
async def alert_currency(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(alert_currency=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_rate_type)
    await callback.message.edit_text("Выберите тип курса:", reply_markup=get_alert_rate_type_keyboard())


@router.callback_query(F.data.startswith("alert_rate_type:"))
async def alert_rate_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(alert_rate_type=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_condition)
    await callback.message.edit_text("Выберите условие:", reply_markup=get_alert_condition_keyboard())


@router.callback_query(F.data.startswith("alert_condition:"))
async def alert_condition(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(alert_condition=callback.data.split(":", 1)[1])
    await state.set_state(MainStates.alert_target_rate)
    await callback.message.edit_text("Введите желаемый курс:")


@router.message(MainStates.alert_target_rate)
async def alert_target_rate(message: Message, state: FSMContext) -> None:
    await state.update_data(alert_target_rate=message.text)
    data = await state.get_data()
    text = (
        "Проверьте уведомление:\n\n"
        f"Валюта: {data.get('alert_currency')}\n"
        f"Тип курса: {data.get('alert_rate_type')}\n"
        f"Условие: {data.get('alert_condition')}\n"
        f"Желаемый курс: {data.get('alert_target_rate')}"
    )
    await state.set_state(MainStates.alert_confirmation)
    await message.answer(text, reply_markup=get_alert_keyboard("confirm"))


@router.callback_query(F.data == "confirm_alert")
async def confirm_alert(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    branch_id = user.get("branch_id") if user else None
    await add_rate_alert(callback.from_user.id, branch_id or "", data.get("alert_currency"), data.get("alert_rate_type"), data.get("alert_condition"), data.get("alert_target_rate"))
    await callback.message.answer("Уведомление сохранено.")
    await state.clear()


@router.callback_query(F.data == "delete_all_alerts")
async def delete_all_alerts(callback: CallbackQuery) -> None:
    await deactivate_all_alerts(callback.from_user.id)
    await callback.message.edit_text("Все уведомления отключены.", reply_markup=get_main_menu_keyboard())
