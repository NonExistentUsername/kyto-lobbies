import factories
import pytest
from domain import commands
from service_player import exceptions, messagebus


def bootstrap_test_message_bus() -> messagebus.MessageBus:
    ram_uow = factories.create_uow("ram")
    return factories.create_message_bus(
        uow=ram_uow,
    )


class TestPlayerCreation:
    def test_create_player(self):  # sourcery skip: class-extract-method
        message_bus = bootstrap_test_message_bus()

        message_bus.handle(commands.CreatePlayer(username="test"))
        assert message_bus.uow.players.get(username="test") is not None

    def test_cannot_create_player_with_same_username(self):
        message_bus = bootstrap_test_message_bus()

        message_bus.handle(commands.CreatePlayer(username="test"))
        assert message_bus.uow.players.get(username="test") is not None
        with pytest.raises(exceptions.PlayerAlreadyExists):
            message_bus.handle(commands.CreatePlayer(username="test"))
        assert len(message_bus.uow.players) == 1

    def test_cannot_create_player_with_empty_username(self):
        message_bus = bootstrap_test_message_bus()

        with pytest.raises(exceptions.InvalidPlayerUsername):
            message_bus.handle(commands.CreatePlayer(username=""))
