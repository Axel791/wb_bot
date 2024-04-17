from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.telegram_user_service import TelegramUserService

from app.schemas.telegram_user import TelegramUserEntity

start_router = Router()


@start_router.message(CommandStart())
@inject
async def command_start(
    message: Message,
    telegram_user_service: TelegramUserService = Provide[
        Container.telegram_user_service
    ],
) -> None:
    user_dict = message.from_user.model_dump()
    args = message.text.split(maxsplit=1)
    deep_link_arg = None
    if len(args) > 1:
        deep_link_arg = args[1]

    user_id = user_dict.pop("id")

    user_dict["referrer_id"] = deep_link_arg
    user_dict["user_id"] = user_id

    user = TelegramUserEntity(**user_dict)

    await telegram_user_service.create_telegram_user(user=user)
    await message.answer(f"Hello world")
