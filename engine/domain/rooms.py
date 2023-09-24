from typing import List, Optional

from domain.base import BaseModel
from domain.players import Player


class Room(BaseModel):
    def __init__(
        self, id: str, creator_id: str, players: Optional[List[Player]] = None
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
    def players(self) -> list[Player]:
        """
        Getter for players

        Returns:
            list[Player]: players
        """
        return self.__players

    def add_player(self, player: Player) -> None:
        """
        Add player to room

        Args:
            player (players.Player): Player to add
        """
        self.__players.append(player)
