import httpx
import logging

from app.schemas.supplier_stat_schema import OrderSchema, SaleSchema


logger = logging.Logger(__name__)


class StatisticsAPIService:
    """Сервис для получения статистики по поставщикам через API Wildberries."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

        self._client = httpx.AsyncClient(headers={"Authorization": self._api_key})

    async def _get_data(self, endpoint: str, date_from: str, flag: int = 0) -> list[dict] | None:
        """Общий метод для получения данных с использованием фильтров."""
        try:
            params = {
                "dateFrom": date_from,
                "flag": flag
            }
            response = await self._client.get(f"{self._base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPStatusError, httpx.RequestError, Exception) as _exc:
            logger.error(f"ERROR: {_exc}")
            return None

    async def get_sales_data(self, date_from: str, flag: int = 0) -> list[SaleSchema] | None:
        """Получение данных о продажах."""
        data = await self._get_data("/api/v1/supplier/sales", date_from, flag)
        if data:
            return [SaleSchema(**obj) for obj in data]
        return None

    async def get_orders_data(self, date_from: str, flag: int = 0) -> list[OrderSchema] | None:
        """Получение данных о заказах."""
        data = await self._get_data("/api/v1/supplier/orders", date_from, flag)
        if data:
            return [OrderSchema(**obj) for obj in data]
        return None

    async def close(self):
        """Закрытие клиента HTTP."""
        await self._client.aclose()
