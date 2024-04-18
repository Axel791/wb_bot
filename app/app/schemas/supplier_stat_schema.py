from pydantic import BaseModel, Field

from datetime import datetime

from app.models.supplier_stat import OrderType


class TransactionBaseSchema(BaseModel):
    date: datetime = Field(..., alias="date", title="Дата транзакции")
    last_change_date: datetime = Field(..., alias="lastChangeDate", title="Дата последнего изменения")
    warehouse_name: str = Field(..., alias="warehouseName", title="Название склада")
    country_name: str = Field(..., alias="countryName", title="Страна")
    oblast_okrug_name: str = Field(..., alias="oblastOkrugName", title="Федеральный округ")
    region_name: str = Field(..., alias="regionName", title="Регион")
    supplier_article: str = Field(..., alias="supplierArticle", title="Артикул поставщика")
    nm_id: int = Field(..., alias="nmId", title="Внутренний ID товара")
    barcode: str = Field(..., alias="barcode", title="Штрихкод товара")
    category: str = Field(..., alias="category", title="Категория товара")
    subject: str = Field(..., alias="subject", title="Подкатегория товара")
    brand: str = Field(..., alias="brand", title="Бренд")
    tech_size: str = Field(..., alias="techSize", title="Технический размер")
    income_id: int = Field(..., alias="incomeID", title="ID поступления товара")
    is_supply: bool = Field(..., alias="isSupply", title="Признак поставки")
    is_realization: bool = Field(..., alias="isRealization", title="Признак реализации")
    total_price: float = Field(..., alias="totalPrice", title="Общая стоимость")
    discount_percent: int = Field(..., alias="discountPercent", title="Процент скидки")
    spp: float = Field(..., alias="spp", title="Стоимость после специальной скидки")
    finished_price: float = Field(..., alias="finishedPrice", title="Окончательная цена")
    price_with_disc: float = Field(..., alias="priceWithDisc", title="Цена с учетом скидки")
    sticker: str | None = Field(None, alias="sticker", title="Номер наклейки")
    g_number: str | None = Field(None, alias="gNumber", title="Глобальный номер товара")
    order_type: OrderType = Field(..., alias="orderType", title="Тип заказа")
    srid: str | None = Field(None, alias="srid", title="Уникальный идентификатор источника данных")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class OrderSchema(TransactionBaseSchema):
    is_cancel: bool | None = Field(None, alias="isCancel", title="Признак отмены")
    cancel_date: datetime | None = Field(None, alias="cancelDate", title="Дата отмены")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class SaleSchema(TransactionBaseSchema):
    payment_sale_amount: float = Field(..., alias="paymentSaleAmount", title="Сумма платежа по продаже")
    for_pay: float = Field(..., alias="fowrPay", title="Сумма к оплате")
    sale_id: str = Field(..., alias="saleID", title="Уникальный ID продажи")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
