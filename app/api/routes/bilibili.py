from fastapi import APIRouter, Depends, Query
from pydantic import HttpUrl
from starlette.background import BackgroundTasks

from app.api.dependencies.create import get_create_from_dict
from app.api.dependencies.database import get_repository
from app.db.repositories.bilibili import UpRepository
from app.models.schemas.bilibili import ListOfUpsInResponse, UpInCreate, UpInDB
from app.spider.bilibili.up import get_up_info, update_up_info, multi_up_info

router = APIRouter()


@router.get("/ups", response_model=ListOfUpsInResponse, name="bilibili:get-ups")
async def get_ups(
        limit: int = Query(20, gt=0),
        offset: int = Query(0, ge=0),
        up_repo: UpRepository = Depends(get_repository(UpRepository))
) -> ListOfUpsInResponse:
    ups = await up_repo.get_ups(limit=limit, offset=offset)

    return ListOfUpsInResponse(ups=ups)


@router.get("/add-up", response_model=UpInDB, name="bilibili:add-up")
async def add_up(
        background_tasks: BackgroundTasks,
        url: HttpUrl = Query(...),
        up_repo: UpRepository = Depends(get_repository(UpRepository))
) -> UpInDB:
    up_info = await get_up_info(url=url)
    create = get_create_from_dict(CREATE_MODEL=UpInCreate)(up_info)
    up_in_db = await up_repo.create(CREATE_MODEL=UpInCreate, RETURN_MODEL=UpInDB)(create)
    background_tasks.add_task(update_up_info, url=url, up_repo=up_repo)

    return up_in_db

@router.get("/multi", name="bilibili:multi")
async def multi(background_tasks: BackgroundTasks,up_repo: UpRepository = Depends(get_repository(UpRepository))):

    background_tasks.add_task(multi_up_info, up_repo=up_repo)

    return {"mgs": "success"}