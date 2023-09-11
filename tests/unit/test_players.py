import factories
from domain import commands, players
from service_player import exceptions, messagebus


def bootstrap_test_message_bus() -> messagebus.MessageBus:
    ram_uow = factories.create_uow("ram")
    return factories.create_message_bus(
        uow=ram_uow,
    )


class TestPlayerCreation:
    def test_create_player(self):  # sourcery skip: class-extract-method
        message_bus = bootstrap_test_message_bus()

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        command_result: commands.CommandResult = future_result.await_result()

        assert future_result is not None
        assert future_result.result is not None

        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, players.Player)

        assert message_bus.uow.players.get(username="test") is not None

    def test_cannot_create_player_with_same_username(self):
        message_bus = bootstrap_test_message_bus()

        message_bus.handle(commands.CreatePlayer(username="test"))
        assert message_bus.uow.players.get(username="test") is not None

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        command_result: commands.CommandResult = future_result.await_result()

        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, exceptions.PlayerAlreadyExists)

        assert len(message_bus.uow.players) == 1

    def test_cannot_create_player_with_empty_username(self):
        message_bus = bootstrap_test_message_bus()

        future_result: messagebus.FutureResult = message_bus.handle(
            commands.CreatePlayer(username="")
        )
        command_result: commands.CommandResult = future_result.await_result()

        assert command_result is not None
        assert command_result.result is not None
        assert isinstance(command_result.result, exceptions.InvalidPlayerUsername)
