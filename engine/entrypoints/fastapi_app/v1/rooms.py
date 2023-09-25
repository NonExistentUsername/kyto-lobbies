import logging
import multiprocessing.pool
from typing import Annotated, List, Union

from domain import commands, rooms
from entrypoints.fastapi_app.deps import get_message_bus
from entrypoints.fastapi_app.responses import (
    ErrorResponse,
    GetRoomResponse,
    InternalErrorResponse,
    Response,
    Room,
)
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
    creator_id: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Create room endpoint

    It will create room with creator as player with creator_id
    """
    try:
        async_result: multiprocessing.pool.AsyncResult = message_bus.handle(
            commands.CreateRoom(creator_id=creator_id)
        )
        room: rooms.Room = async_result.get()

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
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_409_CONFLICT,
            ).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
    except exceptions.PlayerDoesNotExist as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=ErrorResponse(
                message="Internal server error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(
    "/{room_id}/join",
    response_model=Response,
    status_code=status.HTTP_200_OK,
)
async def join_room(
    room_id: str,
    player_id: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Join room endpoint

    It will add player with player_id to room with room_id
    """
    try:
        async_result: multiprocessing.pool.AsyncResult = message_bus.handle(
            commands.JoinRoom(room_id=room_id, player_id=player_id)
        )
        room: rooms.Room = async_result.get()

        return JSONResponse(
            content=Response(
                message="Player joined room",
                data={
                    "id": room.id,
                    "creator_id": room.creator_id,
                },
                status_code=status.HTTP_200_OK,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except exceptions.RoomDoesNotExist as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except exceptions.PlayerDoesNotExist as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except exceptions.PlayerAlreadyInRoom as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_409_CONFLICT,
            ).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=InternalErrorResponse().model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/{room_id}",
    response_model=Response,
    status_code=status.HTTP_200_OK,
)
async def get_room(
    room_id: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Get room endpoint

    It will return room with room_id
    """
    room: rooms.Room = message_bus.uow.rooms.get(id=room_id)

    if room is None:
        return JSONResponse(
            content=ErrorResponse(
                message="Room does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    players: List[str] = [player.id for player in room.players]

    return JSONResponse(
        content=GetRoomResponse(
            message="Room found",
            data=Room(
                id=room.id,
                creator_id=room.creator_id,
                players=players,
            ),
            status_code=status.HTTP_200_OK,
            success=True,
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/{room_id}/leave",
    response_model=Response,
    status_code=status.HTTP_200_OK,
)
async def leave_room(
    room_id: str,
    player_id: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Leave room endpoint

    It will remove player with player_id from room with room_id
    """
    try:
        async_result: multiprocessing.pool.AsyncResult = message_bus.handle(
            commands.LeaveRoom(room_id=room_id, player_id=player_id)
        )
        room: rooms.Room = async_result.get()

        return JSONResponse(
            content=Response(
                message="Player left room",
                data={
                    "id": room.id,
                    "creator_id": room.creator_id,
                },
                status_code=status.HTTP_200_OK,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except exceptions.RoomDoesNotExist as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except exceptions.PlayerDoesNotExist as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except exceptions.PlayerNotInRoom as e:
        return JSONResponse(
            content=ErrorResponse(
                message=str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=InternalErrorResponse().model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
