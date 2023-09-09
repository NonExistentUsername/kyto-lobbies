from pydantic import BaseModel


class Response(BaseModel):
    """
    Basic response model
    """

    message: str
    status_code: int
    success: bool
