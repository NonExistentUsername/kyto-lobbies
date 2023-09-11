from dataclasses import dataclass


class Event:
    pass


@dataclass
class PlayerCreated(Event):
    id: str
    username: str


@dataclass
class RoomCreated(Event):
    id: str
    creator_id: str
