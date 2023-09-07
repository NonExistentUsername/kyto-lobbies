from uuid import UUID
from domain.player import Player


class Room:
    def __init__(self, id: UUID, players: list[Player]):
        self.__id = id
        self.__players = players

    @property
    def id(self) -> UUID:
        """
        Getter for id

        Returns:
            UUID: id
        """
        return self.__id

    @property
    def players(self) -> list[Player]:
        """
        Getter for players

        Returns:
            list[Player]: players
        """
        return self.__players
