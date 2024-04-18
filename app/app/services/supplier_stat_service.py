from enum import Enum

from app.repositories.supplier_stat_repository import RepositorySupplierSale, RepositorySupplierOrder
from app.schemas.supplier_stat_schema import SaleSchema, OrderSchema


class StatType(Enum):
    orders = "ORDERS"
    sales = "SALES"


class SupplierStatService:
    """Сервис статистики поставщиков."""

    def __init__(
            self,
            repository_supplier_order: RepositorySupplierOrder,
            repository_supplier_sale: RepositorySupplierSale
    ) -> None:
        self._repository_supplier_order = repository_supplier_order
        self._repository_supplier_sale = repository_supplier_sale

    async def validate_exist_stat_item(self, objs: list[OrderSchema | SaleSchema], stat_type: StatType) -> list[dict]:
        """Валидация существующих заказов/продаж"""
        dict_data = [dict_obj.model_dump() for dict_obj in objs]
        new_objs = []
        for obj in dict_data:
            exists = await (
                self._repository_supplier_order
                if stat_type == StatType.orders else self._repository_supplier_sale).exists(**obj)
            if not exists:
                new_objs.append(obj)
        return new_objs

    async def create_supplier_orders_stat(self, objs: list[dict]) -> None:
        """Сохранение информации о новых заказах"""
        await self._repository_supplier_order.bulk_create(objs_in=objs)

    async def create_supplier_sale_stat(self, objs: list[dict]) -> None:
        """Сохранение информации о новых продажах"""
        await self._repository_supplier_sale.bulk_create(objs_in=objs)
