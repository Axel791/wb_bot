import time

from aiogram.types import Message

from app.core.config import settings

from loguru import logger


async def rate_limit_middleware(handler, event: Message, data: dict):
    """Middleware для ограничения отправки сообщений пользователем боту."""

    user_id = event.from_user.id
    current_time = time.time()

    if not hasattr(rate_limit_middleware, "users"):
        rate_limit_middleware.users = {}

    if user_id in rate_limit_middleware.users:
        last_message_time = rate_limit_middleware.users[user_id]

        if current_time - last_message_time < settings.message_per_second:
            return await event.answer("Слишком много сообщений! Попробуйте позже.")

    rate_limit_middleware.users[user_id] = current_time
    return await handler(event, data)
