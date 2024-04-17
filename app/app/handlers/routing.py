from aiogram import Router

from .start import start_router


def get_all_routers() -> Router:
    """Функция для регистрации всех router"""

    router = Router()
    router.include_router(start_router)

    return router
