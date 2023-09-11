from dataclasses import dataclass
from uuid import uuid4

from domain import players, rooms


class Event:
    def __init__(self):
        self.id: str = str(uuid4())  # unique id of event


@dataclass
class PlayerCreated(Event):
    player: players.Player


@dataclass
class RoomCreated(Event):
    room: rooms.Room
