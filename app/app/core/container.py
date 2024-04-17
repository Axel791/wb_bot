from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import AsyncSessionConstructor

from app.repositories.telegram_user import RepositoryTelegramUser

from app.models.telegram_user import TelegramUser

from app.services.telegram_user_service import TelegramUserService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(AsyncSessionConstructor, db_url=config.provided.postgres_url)
    session = providers.Factory(db().create_session)

    # region repository
    repository_telegram_user = providers.Singleton(
        RepositoryTelegramUser, model=TelegramUser, session=session
    )
    # endregion

    # region services
    telegram_user_service = providers.Singleton(
        TelegramUserService, repository_telegram_user=repository_telegram_user
    )
    # endregion
