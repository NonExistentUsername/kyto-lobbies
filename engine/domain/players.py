from typing import TYPE_CHECKING

from domain.base import BaseModel

if TYPE_CHECKING:
    from domain.events import Event


class Player(BaseModel):
    def __init__(self, id: str, username: str):
        super().__init__(id)
        self.username: str = username
        self.events: list[Event] = []
