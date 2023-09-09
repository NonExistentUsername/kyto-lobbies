import logging
from typing import Annotated

from domain.commands import CreatePlayer
from entrypoints.fastapi_app.deps import get_message_bus
from fastapi import APIRouter, Depends
from service_player.messagebus import MessageBus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_player(message_bus: Annotated[MessageBus, Depends(get_message_bus)]):
    try:
        result = message_bus.handle_command(CreatePlayer())
        print(result)
    except Exception as e:
        logger.exception(e)
        return {"success": False, "message": "Error creating player"}
    return {"success": True, "message": "Player created successfully"}
