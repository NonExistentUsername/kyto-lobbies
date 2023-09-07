from uuid import UUID
from dataclasses import dataclass


@dataclass
class State:
    pass


class Game:
    def __init__(self, id: UUID, state: State):
        self.__id = id
        self.__state = state

    @property
    def id(self) -> UUID:
        """
        Getter for id

        Returns:
            UUID: id
        """
        return self.__id

    @property
    def state(self) -> State:
        """
        Getter for state

        Returns:
            State: state
        """
        return self.__state
