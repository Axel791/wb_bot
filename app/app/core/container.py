from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import AsyncSessionConstructor

from app.repositories.telegram_user import RepositoryTelegramUser
from app.repositories.supplier_stat_repository import RepositorySupplierOrder, RepositorySupplierSale

from app.models.telegram_user import TelegramUser
from app.models.supplier_stat import SupplierSale, SupplierOrder

from app.services.telegram_user_service import TelegramUserService
from app.services.supplier_stat_service import SupplierStatService
from app.services.excel_export_service import ExcelExportService
from app.services.statics_api_service import StatisticsAPIService


class Container(containers.DeclarativeContainer):
    """Зависимости проекта"""

    config = providers.Singleton(Settings)
    db = providers.Singleton(AsyncSessionConstructor, db_url=config.provided.postgres_url)
    session = providers.Factory(db().create_session)

    # region repository
    repository_telegram_user = providers.Singleton(
        RepositoryTelegramUser, model=TelegramUser, session=session,
    )
    repository_supplier_order = providers.Singleton(
        RepositorySupplierOrder, model=SupplierOrder, session=session,
    )
    repository_supplier_sale = providers.Singleton(
        RepositorySupplierSale, model=SupplierSale, session=session,
    )
    # endregion

    # region services
    telegram_user_service = providers.Singleton(
        TelegramUserService, repository_telegram_user=repository_telegram_user,
    )
    supplier_stat_service = providers.Singleton(
        SupplierStatService,
        repository_supplier_order=repository_supplier_order,
        repository_supplier_sale=repository_supplier_sale,
    )
    excel_export_service = providers.Singleton(ExcelExportService)
    statics_api_service = providers.Singleton(
        StatisticsAPIService,
        base_url=config.provided.base_url,
        api_key=config.provided.wb_api_key,
    )
    # endregion
