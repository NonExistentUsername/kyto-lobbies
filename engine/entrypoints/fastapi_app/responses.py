from pydantic import BaseModel


class Response(BaseModel):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool
    message: str
    data: dict = {}


class ErrorResponse(BaseModel):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool = False
    message: str
    data: dict = {}


class InternalErrorResponse(BaseModel):
    """
    Basic response model
    """

    status_code: int = 500  # Internal status code
    success: bool = False
    message: str = "Internal server error"
    data: dict = {}
