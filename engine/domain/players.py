from typing import TYPE_CHECKING

from domain.base import BaseModel

if TYPE_CHECKING:
    from domain.events import Event


class Player(BaseModel):
    def __init__(self, id: str, username: str):
        super().__init__(id)
        self.username: str = username
        self.events: list[Event] = []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
