from fastapi import APIRouter, Depends

from engine.entrypoints.fastapi_app.deps import get_current_user

players_router = APIRouter(
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@players_router.post("/")
async def create_player():
    return {"message": "Hello World"}
