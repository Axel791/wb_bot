from .base import RepositoryBase
from app.models.telegram_user import TelegramUser


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):
    """Репозиторий телеграм пользователя"""
