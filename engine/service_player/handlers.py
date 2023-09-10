from uuid import uuid4

from domain import player as players
from service_player import unit_of_work


def create_player(uow: unit_of_work.AbstractRepository) -> players.Player:
    """
    Create player

    Returns:
        player.Player: Player
    """
    with uow:
        player = players.Player(id=str(uuid4()))
        uow.repository.add(player)
        uow.commit()

    return player
