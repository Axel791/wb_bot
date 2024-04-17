import asyncio

from loguru import logger

from app.handlers.routing import get_all_routers

from app.middlewares.throttling import rate_limit_middleware
from app.middlewares.session_middleware import SQLAlchemySessionMiddleware

from app.core.container import Container
from app import handlers

from loader import dp, bot


async def main(container: Container):
    """Запуск бота."""
    try:
        async_session = container.session()

        all_routers = get_all_routers()
        dp.include_routers(all_routers)
        dp.message.middleware(rate_limit_middleware)
        dp.message.middleware(SQLAlchemySessionMiddleware(async_session=async_session))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[handlers])
    logger.info("Bot is starting")
    asyncio.run(main(container=container))