import enum

from app.db.base import Base

from app.models.mixins import UUIDMixin, TimestampedMixin
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, BigInteger, Enum


class OrderType(enum.Enum):
    """Типы заказов"""
    client = "Клиентский"
    return_of_marriage = "Возврат брака"
    forced_return = "Принудительный возврат"
    return_of_anonymity = "Возврат обезлички"
    return_invalid_attachment = "Возврат Неверного Вложения"
    seller_return = "Возврат продавца"


class TransactionBase(UUIDMixin, TimestampedMixin):
    """Базовая модель для хранения транзакций (заказов и продаж)."""

    date = Column(DateTime, nullable=False, doc="Дата транзакции.")
    last_change_date = Column(DateTime, nullable=False, doc="Дата последнего изменения транзакции.")
    warehouse_name = Column(String(255), nullable=False, doc="Название склада.")
    country_name = Column(String(255), nullable=False, doc="Страна.")
    oblast_okrug_name = Column(String(255), nullable=False, doc="Федеральный округ.")
    region_name = Column(String(255), nullable=False, doc="Регион.")
    supplier_article = Column(String(255), nullable=False, doc="Артикул поставщика.")
    nm_id = Column(BigInteger, nullable=False, doc="Внутренний ID товара.")
    barcode = Column(String(255), nullable=False, doc="Штрихкод товара.")
    category = Column(String(255), nullable=False, doc="Категория товара.")
    subject = Column(String(255), nullable=False, doc="Подкатегория товара.")
    brand = Column(String(255), nullable=False, doc="Бренд товара.")
    tech_size = Column(String(255), nullable=False, doc="Технический размер товара.")
    income_id = Column(BigInteger, nullable=False, doc="ID поступления товара.")
    is_supply = Column(Boolean, default=False, nullable=False, doc="Признак поставки товара.")
    is_realization = Column(Boolean, default=True, nullable=False, doc="Признак реализации товара.")
    total_price = Column(Float, nullable=False, doc="Общая стоимость товара.")
    discount_percent = Column(Integer, nullable=False, doc="Процент скидки на товар.")
    spp = Column(Float, nullable=False, doc="Стоимость товара после применения специальной скидки.")
    finished_price = Column(Float, nullable=False, doc="Окончательная цена товара.")
    price_with_disc = Column(Float, nullable=False, doc="Цена товара с учетом скидки.")
    order_type = Column(Enum(OrderType), nullable=False, doc="Тип заказа.")
    sticker = Column(String(255), nullable=True, doc="Номер наклейки.")
    g_number = Column(String(255), nullable=True, doc="Глобальный номер товара.")
    srid = Column(String(255), nullable=True, doc="Уникальный идентификатор источника данных.")


class SupplierOrder(TransactionBase, Base):
    """Модель заказов"""

    is_cancel = Column(Boolean, default=False, doc="Признак отмены")
    cancel_date = Column(DateTime, nullable=False, doc="Дата отмены")

    __tablename__ = "order"

    def __repr__(self):
        return f"Заказ: {self.supplier_article}"


class SupplierSale(TransactionBase, Base):
    """Модель продаж"""

    __tablename__ = "sale"

    payment_sale_amount = Column(Float, nullable=False, doc="Сумма платежа по продаже.")
    for_pay = Column(Float, nullable=False, doc="Сумма к оплате.")
    sale_id = Column(String(255), nullable=False, doc="Уникальный ID продажи.")

    def __repr__(self):
        return f"Продажа: {self.supplier_article}"
