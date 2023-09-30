from typing import Any, Dict

from domain.base import BaseModel


class GameDescription(BaseModel):
    def __init__(self, id: str, name: str, description: str):
        super().__init__(id)
        self.__name = name
        self.__description = description

    @property
    def name(self) -> str:
        """
        Getter for name

        Returns:
            str: name
        """
        return self.__name

    @property
    def description(self) -> str:
        """
        Getter for description

        Returns:
            str: description
        """
        return self.__description


class Game(BaseModel):
    def __init__(self, id: str, game_description_id: str, state: Dict[str, Any]):
        super().__init__(id)
        self.__game_description_id = game_description_id
        self.__state = state

    @property
    def game_description_id(self) -> str:
        """
        Getter for game_description_id

        Returns:
            str: game_description_id
        """
        return self.__game_description_id

    @property
    def state(self) -> Dict[str, Any]:
        """
        Getter for state

        Returns:
            State: state
        """
        return self.__state
