from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreatePlayer(Command):
    external_id: str
