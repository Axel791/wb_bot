import asyncio

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)


class AsyncSessionConstructor:

    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(str(db_url))
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)
        self.session = async_scoped_session(self.session_factory, asyncio.current_task)

    def create_session(self) -> AsyncSession:
        return self.session()
