import logging
from typing import Annotated, Union

from domain.commands import CreatePlayer
from entrypoints.fastapi_app.deps import get_message_bus
from entrypoints.fastapi_app.response import Response
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from service_player.messagebus import MessageBus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_player(
    message_bus: Annotated[MessageBus, Depends(get_message_bus)]
) -> Union[JSONResponse, Response]:
    try:
        result = message_bus.handle_command(CreatePlayer())
        print(result)
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
