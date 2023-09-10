from dataclasses import dataclass


class Event:
    pass


@dataclass
class PlayerCreated(Event):
    id: str
    username: str
