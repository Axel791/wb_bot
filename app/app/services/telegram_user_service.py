from app.repositories.telegram_user import RepositoryTelegramUser
from app.schemas.telegram_user import TelegramUserEntity


class TelegramUserService:

    def __init__(self, repository_telegram_user: RepositoryTelegramUser) -> None:
        self._repository_telegram_user = repository_telegram_user

    async def create_telegram_user(self, user: TelegramUserEntity) -> None:
        user_exist = await self._repository_telegram_user.exists(user_id=user.user_id)
        if not user_exist:
            await self._repository_telegram_user.create(obj_in=user.model_dump())
