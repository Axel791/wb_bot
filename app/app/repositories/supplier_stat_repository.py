from .base import RepositoryBase
from app.models.supplier_stat import SupplierOrder, SupplierSale


class RepositorySupplierOrder(RepositoryBase[SupplierOrder]):
    """Репозиторий заказа"""


class RepositorySupplierSale(RepositoryBase[SupplierSale]):
    """Репозиторий продажи"""
