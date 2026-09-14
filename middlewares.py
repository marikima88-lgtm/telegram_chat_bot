from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from database import get_user_language
from i18n import normalize_language


class LanguageMiddleware(BaseMiddleware):
    """Передаёт в обработчики язык пользователя как аргумент `lang`."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        language = await get_user_language(user.id) if user else None
        data["lang"] = normalize_language(language)
        return await handler(event, data)
