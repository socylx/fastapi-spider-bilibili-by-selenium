from time import sleep

from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


def test_func(background_tasks: BackgroundTasks):
    def func(num):
        for i in range(100):
            print(f"num: {num}, number: {i}")
            sleep(0.2)
    background_tasks.add_task(func, num=1)
    background_tasks.add_task(func, num=2)
    background_tasks.add_task(func, num=3)


@router.get("")
async def test(background_tasks: BackgroundTasks):

    test_func(background_tasks)

    return {"msg": "success"}
