from uuid import UUID
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio.session import AsyncSession


ModelType = TypeVar("ModelType")


class RepositoryBase(Generic[ModelType,]):
    """Репозиторий с базовым CRUD"""

    def __init__(self, model: Type[ModelType], session) -> None:
        self._model = model
        self._session: AsyncSession = session

    async def create(self, obj_in: dict) -> ModelType:
        statement = insert(self._model).values(**obj_in).returning(self._model)

        res = await self._session.execute(statement)
        return res.scalar_one()

    async def bulk_create(self, objs_in: list[dict]) -> None:
        instances = [self._model(**data) for data in objs_in]
        if not self._session.in_transaction():
            async with self._session.begin():
                self._session.add_all(instances)
        else:
            self._session.add_all(instances)
            await self._session.flush()

    async def get(
        self,
        *args,
        **kwargs,
    ) -> Optional[ModelType]:
        statement = select(self._model).filter(*args).filter_by(**kwargs)
        res = await self._session.execute(statement)
        return res.scalars().first()

    async def list(self, *args, **kwargs):
        statement = select(self._model).filter(*args).filter_by(**kwargs)
        res = await self._session.execute(statement)
        return res.scalars().all()

    async def update(self, *, obj_id: UUID, obj_in) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        statement = (
            update(self._model)
            .where(self._model.id == obj_id)
            .values(**update_data)
            .returning(self._model)
        )
        update_model = await self._session.execute(statement)
        return update_model.scalar_one()

    async def delete(self, *args, obj_id: UUID, **kwargs) -> None:
        statement = delete(self._model).where(self._model.id == obj_id)
        await self._session.execute(statement)

    async def exists(self, *args, **kwargs) -> bool:
        try:
            statement = select(self._model).filter(*args).filter_by(**kwargs)
            res = await self._session.execute(statement)
            res.scalar_one()
            return True
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return False
