from dataclasses import dataclass
from uuid import uuid4


class Command:
    def __init__(self):
        self.id: str = str(uuid4())  # unique id of command


@dataclass
class CreatePlayer(Command):
    username: str


@dataclass
class CreateRoom(Command):
    creator_id: str  # id of player who created the room
