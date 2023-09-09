from entrypoints.fastapi_app.v1.players import router as players_router
from fastapi import APIRouter

router = APIRouter(
    prefix="/v1",
    tags=["api_v1"],
    responses={404: {"description": "Not found"}},
)

router.include_router(players_router)
