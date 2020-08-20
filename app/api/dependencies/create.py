from typing import Type, Callable, Any

from fastapi import Body, Depends

from app.models.domain.rwmodel import DateTimeRWModel


def get_create_from_body(CREATE_MODEL: Type[DateTimeRWModel], alias: str, embed=True) -> Callable:
    def _get_create(create: CREATE_MODEL = Body(..., embed=embed, alias=alias)) -> DateTimeRWModel:
        create.set_datetime()
        return create

    return _get_create


def get_create_from_dict(CREATE_MODEL: Type[DateTimeRWModel]) -> Callable:
    def _get_create(CREATE: dict) -> DateTimeRWModel:
        create = CREATE_MODEL(**CREATE)
        create.set_datetime()
        return create

    return _get_create
