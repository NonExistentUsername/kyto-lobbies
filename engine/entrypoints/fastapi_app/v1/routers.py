from entrypoints.fastapi_app.v1.players import router as players_router
from entrypoints.fastapi_app.v1.rooms import router as rooms_router
from fastapi import APIRouter

"""
Here we will include all routers
"""

router = APIRouter(
    prefix="/v1",
    tags=["api_v1"],
)

router.include_router(players_router)
router.include_router(rooms_router)
