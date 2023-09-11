import factories
import pytest
from domain import commands, players
from service_player import exceptions, messagebus


def bootstrap_test_message_bus() -> messagebus.MessageBus:
    ram_uow = factories.create_uow("ram")
    return factories.create_message_bus(
        uow=ram_uow,
    )


class TestRoomCreation:
    def test_create_room(self):  # sourcery skip: class-extract-method
        message_bus = bootstrap_test_message_bus()

        message_bus.handle(commands.CreatePlayer(username="test"))
        player: players.Player = message_bus.uow.players.get(username="test")

        message_bus.handle(commands.CreateRoom(creator_id=player.id))
        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None

    def test_cannot_create_room_with_invalid_creator_id(self):
        messagebus = bootstrap_test_message_bus()

        player_id = "123"
        with pytest.raises(exceptions.PlayerDoesNotExist):
            messagebus.handle(commands.CreateRoom(creator_id=player_id))

        assert len(messagebus.uow.rooms) == 0
        assert messagebus.uow.rooms.get(creator_id=player_id) is None

    def test_cannot_create_room_with_same_creator_id(self):
        message_bus = bootstrap_test_message_bus()

        message_bus.handle(commands.CreatePlayer(username="test"))
        player: players.Player = message_bus.uow.players.get(username="test")

        with pytest.raises(exceptions.RoomAlreadyExists):
            message_bus.handle(commands.CreateRoom(creator_id=player.id))
            message_bus.handle(commands.CreateRoom(creator_id=player.id))

        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None
