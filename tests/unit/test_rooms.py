import multiprocessing.pool

import factories
import pytest
from domain import commands, players, rooms
from service_player import exceptions, messagebus


def bootstrap_test_message_bus() -> messagebus.MessageBus:
    ram_uow = factories.create_uow("ram")
    return factories.create_message_bus(
        uow=ram_uow,
    )


class TestRoomCreation:
    def test_create_room(self):  # sourcery skip: class-extract-method
        message_bus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        async_result.get()  # Wait for result
        player: players.Player = message_bus.uow.players.get(username="test")

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()  # Wait for result

        assert async_result.ready()
        assert room is not None
        assert isinstance(room, rooms.Room)

        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None

    def test_cannot_create_room_with_invalid_creator_id(self):
        message_bus = bootstrap_test_message_bus()

        player_id = "123"
        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreateRoom(creator_id=player_id)
        )
        with pytest.raises(exceptions.PlayerDoesNotExist):
            async_result.get()

        assert async_result.ready()

        assert len(message_bus.uow.rooms) == 0
        assert message_bus.uow.rooms.get(creator_id=player_id) is None

    def test_cannot_create_room_with_same_creator_id(self):
        message_bus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        assert async_result.ready()

        async_result: multiprocessing.pool.AsyncResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        assert async_result.ready()
        assert room is not None
        assert isinstance(room, rooms.Room)

        async_result: multiprocessing.pool.AsyncResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )

        with pytest.raises(exceptions.RoomAlreadyExists):
            async_result.get()

        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None
