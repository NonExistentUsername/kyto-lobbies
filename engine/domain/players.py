from domain.base import BaseModel


class Player(BaseModel):
    def __init__(self, id: str):
        super().__init__(id)
