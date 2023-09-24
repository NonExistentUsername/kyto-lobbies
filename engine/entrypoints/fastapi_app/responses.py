from typing import Any, Dict, List

from pydantic import BaseModel


class Room(BaseModel):
    """
    Room model
    """

    id: str
    creator_id: str
    players: List[str]


class Response(BaseModel):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool
    message: str
    data: Dict[str, Any] = {}


class ErrorResponse(Response):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool = False
    message: str


class InternalErrorResponse(ErrorResponse):
    """
    Basic response model
    """

    status_code: int = 500  # Internal status code
    message: str = "Internal server error"


class GetRoomResponse(Response):
    """
    Response model for get room
    """

    data: Room
