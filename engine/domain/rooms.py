from typing import List, Optional

from domain import players as players
from domain.base import BaseModel


class Room(BaseModel):
    def __init__(
        self, id: str, creator_id: str, players: Optional[List[players.Player]] = None
    ):
        super().__init__(id)
        self.__creator_id = creator_id
        self.__players = players or []

    @property
    def creator_id(self) -> str:
        """
        Getter for creator_id

        Returns:
            str: creator_id
        """
        return self.__creator_id

    @property
    def players(self) -> list[players.Player]:
        """
        Getter for players

        Returns:
            list[Player]: players
        """
        return self.__players
