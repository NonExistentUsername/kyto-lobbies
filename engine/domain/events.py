from dataclasses import dataclass
from uuid import uuid4

from domain import players, rooms


class Event:
    def __init__(self):
        self.__id: str = str(uuid4())  # unique id of event

    @property
    def id(self) -> str:
        return self.__id


@dataclass
class PlayerCreated(Event):
    player: players.Player


@dataclass
class RoomCreated(Event):
    room: rooms.Room
