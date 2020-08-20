from fastapi import APIRouter

from app.api.routes import authentication, test, bilibili

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/users")
router.include_router(bilibili.router, tags=["bilibili"], prefix="/bilibili")

router.include_router(test.router, tags=["test"], prefix="/test")
