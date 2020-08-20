from typing import List, Type, Callable

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import UP_COLLECTION_NAME, UP_VIDEO_COLLECTION_NAME, UP_AUDIO_COLLECTION_NAME, \
    UP_ARTICLE_COLLECTION_NAME, UP_ALBUM_COLLECTION_NAME
from app.db.repositories.base import BaseRepository
from app.models.domain.rwmodel import DateTimeRWModel
from app.models.schemas.bilibili import UpInDB


class UpRepository(BaseRepository):
    __collection__ = UP_COLLECTION_NAME

    def __init__(self, conn: AsyncIOMotorClient) -> None:
        super().__init__(conn)
        self._video_repo = UpVideoRepository(conn)
        self._audio_repo = UpAudioRepository(conn)
        self._article_repo = UpArticleRepository(conn)
        self._album_repo = UpAlbumRepository(conn)

    async def get_ups(self, *, limit: int = 20, offset: int = 0) -> List[UpInDB]:
        ups = self.collection.find(limit=limit, skip=offset)

        return [UpInDB(**up) async for up in ups]

    def create(self, *, CREATE_MODEL: Type[DateTimeRWModel], RETURN_MODEL: Type[DateTimeRWModel]) -> Callable:
        async def _create(create: CREATE_MODEL) -> RETURN_MODEL:
            result = await self.collection.insert_one(create.dict())

            return RETURN_MODEL(id_=result.inserted_id, **create.dict())

        return _create

    async def create_contribute_content(
            self,
            *,
            CREATE_MODEL: Type[DateTimeRWModel],
            RETURN_MODEL: Type[DateTimeRWModel],
            create_data: DateTimeRWModel,
            info_mode: str,
    ):
        repo: BaseRepository = eval(f"self._{info_mode}_repo")
        await repo.create(CREATE_MODEL=CREATE_MODEL, RETURN_MODEL=RETURN_MODEL)(create_data)



class UpVideoRepository(BaseRepository):
    __collection__ = UP_VIDEO_COLLECTION_NAME


class UpAudioRepository(BaseRepository):
    __collection__ = UP_AUDIO_COLLECTION_NAME


class UpArticleRepository(BaseRepository):
    __collection__ = UP_ARTICLE_COLLECTION_NAME


class UpAlbumRepository(BaseRepository):
    __collection__ = UP_ALBUM_COLLECTION_NAME
