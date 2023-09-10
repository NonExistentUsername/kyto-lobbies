import logging
from typing import Annotated, Union

from domain.commands import CreatePlayer
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

    It will create player and return uuid of player
    It uses message bus to handle command and return response

    Args:
        username (str): Username of player
        message_bus (Annotated[messagebus.MessageBus, Depends): Message bus

    Returns:
        Union[JSONResponse, Response]: Response object
    """
    try:
        message_bus.handle(CreatePlayer(username=username))
    except exceptions.PlayerAlreadyExists as e:
        logger.exception(e)
        return JSONResponse(
            content=Response(
                message="Player already exists",
                status_code=status.HTTP_409_CONFLICT,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=Response(
                message="Error creating player",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(
        content=Response(
            message="Player created",
            status_code=status.HTTP_201_CREATED,
            success=True,
        ).model_dump(),
        status_code=status.HTTP_201_CREATED,
    )
