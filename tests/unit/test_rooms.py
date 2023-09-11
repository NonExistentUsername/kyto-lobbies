import factories
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

        message_bus.handle(commands.CreatePlayer(username="test"))
        player: players.Player = message_bus.uow.players.get(username="test")

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        command_result: commands.CommandResult = future_result.await_result()
        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, rooms.Room)

        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None

    def test_cannot_create_room_with_invalid_creator_id(self):
        message_bus = bootstrap_test_message_bus()

        player_id = "123"
        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreateRoom(creator_id=player_id)
        )
        command_result: commands.CommandResult = future_result.await_result()

        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, exceptions.PlayerDoesNotExist)

        assert len(message_bus.uow.rooms) == 0
        assert message_bus.uow.rooms.get(creator_id=player_id) is None

    def test_cannot_create_room_with_same_creator_id(self):
        message_bus = bootstrap_test_message_bus()

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        command_result: commands.CommandResult = future_result.await_result()
        assert command_result is not None

        player: players.Player = message_bus.uow.players.get(username="test")

        message_bus.handle(commands.CreateRoom(creator_id=player.id))
        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        assert future_result.await_result() is not None

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreateRoom(creator_id=player.id)
        )
        command_result: commands.CommandResult = future_result.await_result()
        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, exceptions.RoomAlreadyExists)

        assert len(message_bus.uow.rooms) == 1
        assert message_bus.uow.rooms.get(creator_id=player.id) is not None
