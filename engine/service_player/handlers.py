import logging
from uuid import uuid4

from domain import commands, events, players
from service_player import exceptions, unit_of_work

logger = logging.getLogger(__name__)


def create_player(
    command: commands.CreatePlayer, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    """
    Create player

    Args:
        command (commands.CreatePlayer): Create player command
        uow (unit_of_work.AbstractUnitOfWork): Unit of work
    """
    with uow:
        if uow.players.get(username=command.username):
            raise exceptions.PlayerAlreadyExists(
                f"Player with username {command.username} already exists"
            )

        player = players.Player(id=str(uuid4()), username=command.username)
        player.events.append(
            events.PlayerCreated(id=player.id, username=player.username)
        )  # TODO: Create event collector
        uow.players.add(player)
        uow.commit()


def player_created_event_handler(event: events.PlayerCreated) -> None:
    """
    Player created event handler

    Args:
        event (events.PlayerCreated): Player created event
    """
    logger.debug(f"Player {event.id} created. Username: {event.username}")


EVENT_HANDLERS = {
    events.PlayerCreated: [player_created_event_handler],
}
COMMAND_HANDLERS = {
    commands.CreatePlayer: create_player,
}
