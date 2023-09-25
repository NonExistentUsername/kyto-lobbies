from typing import List, Optional

from domain.base import BaseModel
from domain.players import Player


class Room(BaseModel):
    def __init__(
        self, id: str, creator: Player, players: Optional[List[Player]] = None
    ):
        super().__init__(id)
        self.__creator_id = creator.id
        self.__players = players or [creator]

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
            list[Player]: players currently in the room
        """
        return self.__players

    def join(self, player: Player) -> None:
        """
        Add a player to the room.

        Args:
            player (players.Player): The player to add to the room.
        """
        self.__players.append(player)

    def leave(self, player: Player) -> None:
        """
        Remove player from room

        Args:
            player (players.Player): Player to remove from the room
        """
        self.__players.remove(player)
