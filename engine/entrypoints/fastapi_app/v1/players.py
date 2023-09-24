import logging
import multiprocessing.pool
from typing import Annotated, Union

from domain import commands, players
from entrypoints.fastapi_app.deps import get_message_bus
from entrypoints.fastapi_app.responses import Response
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from service_player import exceptions, messagebus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_player(
    username: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Create player endpoint

    It will create player with username
    """
    try:
        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username=username)
        )
        player: players.Player = async_result.get()

        return JSONResponse(
            content=Response(
                message="Player created",
                data={
                    "id": player.id,
                    "username": player.username,
                },
                status_code=status.HTTP_201_CREATED,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except exceptions.PlayerAlreadyExists as e:
        return JSONResponse(
            content=Response(
                message=str(e),
                status_code=status.HTTP_409_CONFLICT,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
    except exceptions.InvalidPlayerUsername as e:
        return JSONResponse(
            content=Response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=Response(
                message="Error during creating player",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
