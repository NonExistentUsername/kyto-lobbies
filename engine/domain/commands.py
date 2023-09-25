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
    def __init__(self, command: Command, result: Any = None):
        self.__id: str = str(uuid4())  # unique id of command response
        self.__command: Command = command  # command that was executed
        self.__result: Any = result  # result of command execution

    @property
    def id(self) -> str:
        return self.__id

    @property
    def command(self) -> Command:
        return self.__command

    @property
    def result(self) -> Any:
        return self.__result


@dataclass
class CreatePlayer(Command):
    username: str

    def __init__(self, username: str = ""):
        super().__init__()
        self.username = username


@dataclass
class CreateRoom(Command):
    creator_id: str  # id of player who created the room

    def __init__(self, creator_id: str):
        super().__init__()
        self.creator_id = creator_id


@dataclass
class JoinRoom(Command):
    room_id: str
    player_id: str

    def __init__(self, room_id: str, player_id: str):
        super().__init__()
        self.room_id = room_id
        self.player_id = player_id


@dataclass
class LeaveRoom(Command):
    room_id: str
    player_id: str

    def __init__(self, room_id: str, player_id: str):
        super().__init__()
        self.room_id = room_id
        self.player_id = player_id
