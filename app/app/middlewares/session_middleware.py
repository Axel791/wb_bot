from contextlib import asynccontextmanager
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio.session import AsyncSession


class SQLAlchemySessionMiddleware(BaseMiddleware):
    """Middleware для commit & close  session"""

    def __init__(self, async_session: AsyncSession):
        super().__init__()
        self._async_session: AsyncSession = async_session

    async def __call__(self, handler, event, data):
        async with self.db_session_maker() as session:
            data["session"] = session
            return await handler(event, data)

    @asynccontextmanager
    async def db_session_maker(self):
        try:
            yield self._async_session
            await self._async_session.commit()
        except Exception as e:
            await self._async_session.rollback()
            raise e
        finally:
            await self._async_session.close()
