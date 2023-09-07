from dataclasses import dataclass


@dataclass
class State:
    pass


class Game:
    def __init__(self, id: str, state: State):
        self.__id = id
        self.__state = state

    @property
    def id(self) -> str:
        """
        Getter for id

        Returns:
            str: id
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
