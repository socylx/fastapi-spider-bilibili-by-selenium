from time import sleep

from loguru import logger

from app.api.dependencies.create import get_create_from_dict

from app.db.repositories.bilibili import UpRepository
from app.models.schemas.bilibili import SING_SCHEMA_IN_CREATE_CLASS, SING_SCHEMA_IN_DB_CLASS, UpInCreate, UpInDB
from app.resources.spider import bilibili
from app.spider.driver import Driver, DriverOpen


async def get_up_info(url: str) -> dict:
    up_id = url.split("/")[-1]

    with Driver(url=url) as driver:
        sleep(2)
        exec(bilibili.UP_EXEC_STATEMENTS)
    exec(bilibili.UP_STRING_EXEC_STATEMENTS)

    return locals()["up"]

async def get_single_url_info(info_mode: str, up_repo: UpRepository, file_name: str):
    with DriverOpen(file_name, 'r') as file:
        id_urls = file.readlines()

    with Driver() as driver:
        for id_url in id_urls:
            up_id, url = id_url.strip().split("-")
            driver.get(url)
            try:
                exec(bilibili.SINGLE_EXEC_STATEMENTS[info_mode])
            except Exception as e:
                logger.error(e)
                with DriverOpen(f"fail/fail-{up_id}-{info_mode}", "a") as file:
                    file.write(id_url)
            else:
                create_class = SING_SCHEMA_IN_CREATE_CLASS[info_mode]
                db_class = SING_SCHEMA_IN_DB_CLASS[info_mode]

                await up_repo.create_contribute_content(
                    CREATE_MODEL=create_class,
                    RETURN_MODEL=db_class,
                    create_data=get_create_from_dict(create_class)(locals()["single_dict"]),
                    info_mode=info_mode
                )
            print(f"{info_mode}: {id_url} - success")


async def update(url: str, info_mode: str, up_repo: UpRepository) -> None:
    up_id = url.split("/")[-1]
    url = f"{url}/{info_mode}"

    with Driver(url=url) as driver:
        sleep(2)
        update_list = []
        exec(bilibili.UPDATE_UP_EXEC_STATEMENTS[info_mode])
        await up_repo.update_one(
            lookup={"up_id": up_id},
            update={"$addToSet": {f"contribution.{info_mode}": {"$each": update_list}}}
        )
        with DriverOpen(f"{up_id}-{info_mode}", 'w') as file:
            try:
                exec(bilibili.EXEC_STATEMENTS[info_mode])
            except Exception as e:
                logger.error(e)
                with DriverOpen(f"fail/fail-{up_id}-{info_mode}s", "a") as file:
                    file.write(url)

        print(f"{info_mode} success")

    await get_single_url_info(info_mode=info_mode, up_repo=up_repo, file_name=f"{up_id}-{info_mode}")



async def update_up_info(url: str, up_repo: UpRepository) -> None:
    await update(url=url, info_mode="video", up_repo=up_repo)
    await update(url=url, info_mode="audio", up_repo=up_repo)
    await update(url=url, info_mode="article", up_repo=up_repo)
    await update(url=url, info_mode="album", up_repo=up_repo)


async def multi_up_info(up_repo: UpRepository):
    with DriverOpen("urls", 'r') as file:
        id_urls = file.readlines()


    for space_url in id_urls:
        url = space_url.strip()
        up_info = await get_up_info(url=url)
        create = get_create_from_dict(CREATE_MODEL=UpInCreate)(up_info)
        await up_repo.create(CREATE_MODEL=UpInCreate, RETURN_MODEL=UpInDB)(create)

        await update_up_info(url=url, up_repo=up_repo)
