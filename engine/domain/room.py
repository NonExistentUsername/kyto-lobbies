from typing import TYPE_CHECKING

from domain.base import BaseModel

if TYPE_CHECKING:
    from domain import player as players


class Room(BaseModel):
    def __init__(self, id: str, players: list[players.Player]):
        super().__init__(id)
        self.__players = players

    @property
    def players(self) -> list[players.Player]:
        """
        Getter for players

        Returns:
            list[Player]: players
        """
        return self.__players
