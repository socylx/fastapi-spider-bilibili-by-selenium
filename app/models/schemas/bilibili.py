from typing import List, Dict

from pydantic import BaseModel

from app.models.common import IDModelMixin
from app.models.domain.rwmodel import BaseRWModel, DateTimeRWModel

contribution_type = List[Dict[str, str]]


class ContributionType(BaseModel):
    video: contribution_type
    audio: contribution_type
    article: contribution_type
    album: contribution_type


class Up(BaseRWModel):
    up_id: str
    name: str
    follow_number: str
    fans_number: str
    total_contributions_number: str
    contribution: ContributionType


class UpInCreate(DateTimeRWModel, Up):
    pass


class UpInDB(IDModelMixin, DateTimeRWModel, Up):
    pass


class ListOfUpsInResponse(BaseRWModel):
    ups: List[UpInDB]


# ---video---

class Video(BaseRWModel):
    up_id: str
    title: str
    view: str
    dm: str
    like: str
    coin: str
    collect: str
    share: str
    comment: str
    url: str


class VideoInCreate(DateTimeRWModel, Video):
    pass


class VideoInDB(IDModelMixin, DateTimeRWModel, Video):
    pass


# ---audio---
class Audio(BaseRWModel):
    up_id: str
    url: str
    title: str
    time: str
    coin: str
    collect: str
    comment: str
    share: str


class AudioInCreate(DateTimeRWModel, Audio):
    pass


class AudioInDB(IDModelMixin, DateTimeRWModel, Audio):
    pass


# ---article---
class Article(BaseRWModel):
    up_id: str
    url: str
    title: str
    create_time: str
    coin: str
    collect: str
    view: str
    like: str
    comment: str


class ArticleInCreate(DateTimeRWModel, Article):
    pass


class ArticleInDB(IDModelMixin, DateTimeRWModel, Article):
    pass


# ---album---
class Album(BaseRWModel):
    up_id: str
    url: str
    description: str
    create_date: str
    view: str
    collect: str
    support: str
    like: str


class AlbumInCreate(DateTimeRWModel, Album):
    pass


class AlbumInDB(IDModelMixin, DateTimeRWModel, Album):
    pass


SING_SCHEMA_IN_CREATE_CLASS = {
    "video": VideoInCreate,
    "audio": AudioInCreate,
    "article": ArticleInCreate,
    "album": AlbumInCreate
}

SING_SCHEMA_IN_DB_CLASS = {
    "video": VideoInDB,
    "audio": AudioInDB,
    "article": ArticleInDB,
    "album": AlbumInDB
}
