from pydantic import BaseModel


class Response(BaseModel):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool
    message: str
    data: dict = {}
