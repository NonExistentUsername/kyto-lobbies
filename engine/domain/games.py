from dataclasses import dataclass

from domain.base import BaseModel


@dataclass
class State:
    pass


class Game(BaseModel):
    def __init__(self, id: str, state: State):
        super().__init__(id)
        self.__state = state

    @property
    def state(self) -> State:
        """
        Getter for state

        Returns:
            State: state
        """
        return self.__state
