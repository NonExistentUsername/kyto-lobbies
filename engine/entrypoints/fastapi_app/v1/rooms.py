import logging
from typing import Annotated, Union

from domain import commands, rooms
from entrypoints.fastapi_app.deps import get_message_bus
from entrypoints.fastapi_app.responses import Response
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from service_player import exceptions, messagebus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_room(
    player_id: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Create room endpoint

    It will create room with creator as player with player_id
    """
    try:
        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreateRoom(creator_id=player_id)
        )
        command_result: commands.CommandResult = future_result.await_result()

        if isinstance(command_result.result, Exception):
            raise command_result.result

        room: rooms.Room = command_result.result

        return JSONResponse(
            content=Response(
                message="Room created",
                data={
                    "id": room.id,
                    "creator_id": room.creator_id,
                },
                status_code=status.HTTP_201_CREATED,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except exceptions.RoomAlreadyExists as e:
        return JSONResponse(
            content=Response(
                message=str(e),
                status_code=status.HTTP_409_CONFLICT,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
    except exceptions.PlayerDoesNotExist as e:
        return JSONResponse(
            content=Response(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=Response(
                message="Internal server error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
