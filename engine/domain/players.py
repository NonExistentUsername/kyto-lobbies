from domain.base import BaseModel


class Player(BaseModel):
    def __init__(self, id: str, username: str):
        super().__init__(id)
        self.username: str = username
