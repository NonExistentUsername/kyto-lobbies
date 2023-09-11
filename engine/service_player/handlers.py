import logging
from uuid import uuid4

from domain import commands, events, players, rooms
from service_player import exceptions, unit_of_work

logger = logging.getLogger(__name__)


def create_player(
    command: commands.CreatePlayer, uow: unit_of_work.AbstractUnitOfWork
) -> players.Player:
    """
    Create player

    Args:
        command (commands.CreatePlayer): Create player command
        uow (unit_of_work.AbstractUnitOfWork): Unit of work
    """
    if command.username == "":
        raise exceptions.InvalidPlayerUsername("Player username cannot be empty")

    with uow:
        if uow.players.get(username=command.username):
            raise exceptions.PlayerAlreadyExists(
                f"Player with username {command.username} already exists"
            )

        player = players.Player(id=str(uuid4()), username=command.username)
        player.events.append(
            events.PlayerCreated(player=player)
        )  # TODO: Create event collector
        uow.players.add(player)
        uow.commit()

        return player


def player_created_event_handler(event: events.PlayerCreated) -> None:
    """
    Player created event handler

    Args:
        event (events.PlayerCreated): Player created event
    """
    logger.debug(f"Player {event.id} created. Username: {event.username}")


def create_room(
    command: commands.CreateRoom, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    """
    Create room

    Args:
        command (commands.CreateRoom): Create room command
        uow (unit_of_work.AbstractUnitOfWork): Unit of work
    """
    with uow:
        player: players.Player = uow.players.get(id=command.creator_id)
        if not player:
            raise exceptions.PlayerDoesNotExist(
                f"Player with id {command.creator_id} does not exist"
            )

        if uow.rooms.get(creator_id=command.creator_id):
            raise exceptions.RoomAlreadyExists(
                f"Room with creator id {command.creator_id} already exists"
            )

        room = rooms.Room(id=str(uuid4()), creator_id=command.creator_id)
        room.events.append(events.RoomCreated(room=room))
        uow.rooms.add(room)
        uow.commit()


EVENT_HANDLERS = {
    events.PlayerCreated: [player_created_event_handler],
    events.RoomCreated: [],
}
COMMAND_HANDLERS = {
    commands.CreatePlayer: create_player,
    commands.CreateRoom: create_room,
}
