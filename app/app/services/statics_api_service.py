import httpx


class StatisticsAPIService:
    """Сервис для получения статистики по поставщикам через API Wildberries."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

        self._client = httpx.AsyncClient(headers={"Authorization": self._api_key})

    async def _get_data(self, endpoint: str, date_from: str, flag: int = 0) -> list[dict]:
        """Общий метод для получения данных с использованием фильтров."""
        params = {
            "dateFrom": date_from,
            "flag": flag
        }
        response = await self._client.get(f"{self._base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    async def get_sales_data(self, date_from: str, flag: int = 0) -> list[dict]:
        """Получение данных о продажах."""
        return await self._get_data("/api/v1/supplier/sales", date_from, flag)

    async def get_orders_data(self, date_from: str, flag: int = 0) -> list[dict]:
        """Получение данных о заказах."""
        return await self._get_data("/api/v1/supplier/orders", date_from, flag)

    async def close(self):
        """Закрытие клиента HTTP."""
        await self._client.aclose()
