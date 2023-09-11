from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from domain import players, rooms


class Event:
    def __init__(self):
        self.__id: str = str(uuid4())  # unique id of event

    @property
    def id(self) -> str:
        return self.__id


class EventResult:
    def __init__(self, event: Event, success: bool, result: Any = None):
        self.__id: str = str(uuid4())  # unique id of event response
        self.__event: Event = event  # event that was executed
        self.__success: bool = success  # whether event was executed successfully
        self.__result: Any = result  # result of event execution

    @property
    def id(self) -> str:
        return self.__id

    @property
    def event(self) -> Event:
        return self.__event

    @property
    def success(self) -> bool:
        return self.__success


@dataclass
class PlayerCreated(Event):
    player: players.Player


@dataclass
class RoomCreated(Event):
    room: rooms.Room
