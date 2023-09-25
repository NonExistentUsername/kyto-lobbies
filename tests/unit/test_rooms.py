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

    def test_join_room(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test2")
        )
        another_player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=another_player.id, room_id=room.id)
        )
        room: rooms.Room = async_result.get()

        assert async_result.ready()
        assert room is not None
        assert isinstance(room, rooms.Room)
        assert len(room.players) == 2
        assert room.players[1].id == another_player.id
        assert room.players[1].username == another_player.username

    def test_creator_already_joined_room(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=player.id, room_id=room.id)
        )
        with pytest.raises(exceptions.PlayerAlreadyInRoom):
            async_result.get()

    def test_join_room_with_same_player(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test2")
        )
        another_player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=another_player.id, room_id=room.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=another_player.id, room_id=room.id)
        )
        with pytest.raises(exceptions.PlayerAlreadyInRoom):
            async_result.get()

    def test_join_room_with_invalid_player_id(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id="invalid", room_id=room.id)
        )
        with pytest.raises(exceptions.PlayerDoesNotExist):
            async_result.get()

    def test_join_room_with_invalid_room_id(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        room_id = "123"
        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=player.id, room_id=room_id)
        )
        with pytest.raises(exceptions.RoomDoesNotExist):
            async_result.get()

    def test_leave_room(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test2")
        )
        another_player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.JoinRoom(player_id=another_player.id, room_id=room.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.LeaveRoom(player_id=another_player.id, room_id=room.id)
        )
        room: rooms.Room = async_result.get()

        assert async_result.ready()
        assert room is not None
        assert isinstance(room, rooms.Room)
        assert len(room.players) == 1
        assert room.players[0].id == player.id
        assert room.players[0].username == player.username

    def test_leave_room_with_invalid_player(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.LeaveRoom(player_id="invalid", room_id=room.id)
        )
        with pytest.raises(exceptions.PlayerDoesNotExist):
            async_result.get()

    def test_leave_room_with_invalid_room(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.LeaveRoom(player_id=player.id, room_id="invalid")
        )
        with pytest.raises(exceptions.RoomDoesNotExist):
            async_result.get()

    def test_leave_room_with_player_not_in_room(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test2")
        )
        another_player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.LeaveRoom(player_id=another_player.id, room_id=room.id)
        )
        with pytest.raises(exceptions.PlayerNotInRoom):
            async_result.get()

    def test_leave_room_with_same_player(self):
        messagebus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        room: rooms.Room = async_result.get()

        async_result: multiprocessing.pool.ApplyResult = messagebus.handle(
            commands.LeaveRoom(player_id=player.id, room_id=room.id)
        )
        room = async_result.get()

        assert async_result.ready()
        assert room is not None
        assert isinstance(room, rooms.Room)
        assert len(room.players) == 0
        assert room.players == []
