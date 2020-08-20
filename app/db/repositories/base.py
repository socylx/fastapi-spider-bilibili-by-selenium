from typing import Callable, Type

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient

from app.core.config import DATABASE
from app.models.domain.rwmodel import DateTimeRWModel


class BaseRepository:
    __collection__ = ""

    def __init__(self, conn: AsyncIOMotorClient) -> None:
        self._collection = conn.get_database(DATABASE).get_collection(self.__collection__)

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    def create(self, *, CREATE_MODEL: Type[DateTimeRWModel], RETURN_MODEL: Type[DateTimeRWModel]) -> Callable:
        async def _create(create: CREATE_MODEL) -> RETURN_MODEL:
            result = await self.collection.insert_one(create.dict())

            return RETURN_MODEL(id_=result.inserted_id, **create.dict())

        return _create

    async def delete(self, *, lookup: dict) -> None:
        await self.collection.delete_many(lookup)

    async def update_one(self, *, lookup: dict, update: dict) -> None:
        update_res = await self.collection.update_one(lookup, update)
