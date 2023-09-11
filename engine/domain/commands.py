from dataclasses import dataclass
from uuid import uuid4


class Command:
    def __init__(self):
        self.__id: str = str(uuid4())  # unique id of command

    @property
    def id(self) -> str:
        return self.__id


@dataclass
class CreatePlayer(Command):
    username: str


@dataclass
class CreateRoom(Command):
    creator_id: str  # id of player who created the room
