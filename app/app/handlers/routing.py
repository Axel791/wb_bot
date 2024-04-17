from aiogram import Router

from .start import start_router
from .stat import stat_router


def get_all_routers() -> Router:
    """Функция для регистрации всех router"""

    router = Router()
    router.include_router(start_router)
    router.include_router(stat_router)

    return router
