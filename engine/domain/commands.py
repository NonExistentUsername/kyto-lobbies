from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreatePlayer(Command):
    username: str
