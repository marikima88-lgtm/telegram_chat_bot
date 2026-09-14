import asyncio
import logging
from datetime import datetime

from aiogram import Bot

from config import ALERT_CHECK_INTERVAL_MINUTES
from database import deactivate_rate_alert, get_user_language, list_active_rate_alerts
from i18n import t
from services.rate_provider import RateProvider

logger = logging.getLogger(__name__)


def should_trigger_alert(current_rate: float | int | str, target_rate: float | int | str, condition_type: str) -> bool:
    try:
        current_value = float(current_rate)
        target_value = float(target_rate)
    except (TypeError, ValueError):
        return False

    # В базе условие хранится как ">=" / "<=" (кнопки «Не ниже» / «Не выше»).
    if condition_type in ("above", ">="):
        return current_value >= target_value
    if condition_type in ("below", "<="):
        return current_value <= target_value
    return False


async def start_notification_worker(bot: Bot) -> None:
    while True:
        try:
            await check_alerts(bot)
        except Exception as exc:
            logger.exception("Ошибка в worker уведомлений: %s", exc)
        await asyncio.sleep(ALERT_CHECK_INTERVAL_MINUTES * 60)


async def check_alerts(bot: Bot) -> None:
    provider = RateProvider()
    alerts = await list_active_rate_alerts()
    for alert in alerts:
        if not alert.get("is_active"):
            continue
        branch_id = alert.get("branch_id") or ""
        currency_code = alert.get("currency_code") or ""
        rate = await provider.get_rate(branch_id, currency_code)
        if not rate:
            continue
        current_rate = rate.get(alert.get("rate_type") or "buy") or rate.get("buy") or rate.get("sell")
        if current_rate is None:
            continue

        if should_trigger_alert(current_rate, alert.get("target_rate") or 0, alert.get("condition_type") or "above"):
            user_id = alert.get("telegram_user_id")
            lang = await get_user_language(user_id)
            await bot.send_message(user_id, t("alert_triggered", lang, code=currency_code, rate=current_rate))
            await deactivate_rate_alert(alert.get("id"))
