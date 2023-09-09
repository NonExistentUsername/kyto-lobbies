from typing import Annotated

from domain.commands import CreatePlayer
from fastapi import APIRouter, Depends
from service_player.messagebus import MessageBus

from engine.entrypoints.fastapi_app.deps import get_message_bus

players_router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "Not found"}},
)


@players_router.post("/")
async def create_player(message_bus: Annotated[MessageBus, Depends(get_message_bus)]):
    try:
        message_bus.handle_command(CreatePlayer())
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Player created successfully"}
