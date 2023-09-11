from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreatePlayer(Command):
    username: str


@dataclass
class CreateRoom(Command):
    creator_id: str  # id of player who created the room
