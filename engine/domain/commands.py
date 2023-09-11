from dataclasses import dataclass
from typing import Any
from uuid import uuid4


class Command:
    def __init__(self):
        self.__id: str = str(uuid4())  # unique id of command

    @property
    def id(self) -> str:
        return self.__id


class CommandResult:
    def __init__(self, command: Command, success: bool, result: Any = None):
        self.__id: str = str(uuid4())  # unique id of command response
        self.__command: Command = command  # command that was executed
        self.__success: bool = success  # whether command was executed successfully
        self.__result: Any = result  # result of command execution

    @property
    def id(self) -> str:
        return self.__id

    @property
    def command(self) -> Command:
        return self.__command

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def result(self) -> Any:
        return self.__result


@dataclass
class CreatePlayer(Command):
    username: str


@dataclass
class CreateRoom(Command):
    creator_id: str  # id of player who created the room
