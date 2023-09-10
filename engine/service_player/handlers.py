from uuid import uuid4

from domain import commands, players
from service_player import unit_of_work


def create_player(uow: unit_of_work.AbstractUnitOfWork) -> players.Player:
    """
    Create player

    Returns:
        player.Player: Player
    """
    with uow:
        player = players.Player(id=str(uuid4()))
        uow.players.add(player)
        uow.commit()

    return player


COMMAND_HANDLERS = {
    commands.CreatePlayer: create_player,
}
