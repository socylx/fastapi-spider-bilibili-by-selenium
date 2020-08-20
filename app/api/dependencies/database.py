from typing import Type, Callable

from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from app.db.repositories.base import BaseRepository


async def _get_db_client(request: Request) -> AsyncIOMotorClient:
    yield request.app.state.db


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncIOMotorClient], BaseRepository]:
    def _get_repo(conn: AsyncIOMotorClient = Depends(_get_db_client)) -> BaseRepository:
        return repo_type(conn)

    return _get_repo

def get_up_repository(info_mode:str):
    pass
