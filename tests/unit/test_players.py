import multiprocessing.pool

import factories
import pytest
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

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        player: players.Player = async_result.get()  # Wait for result

        assert async_result.ready()
        assert player is not None
        assert isinstance(player, players.Player)
        assert player.id is not None
        assert player.username == "test"

        assert message_bus.uow.players.get(username="test") is not None

    def test_cannot_create_player_with_same_username(self):
        message_bus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        async_result.get()  # Wait for result

        assert len(message_bus.uow.players) == 1
        assert message_bus.uow.players.get(username="test") is not None

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="test")
        )
        with pytest.raises(exceptions.PlayerAlreadyExists):
            async_result.get()  # Wait for result

        assert len(message_bus.uow.players) == 1

    def test_cannot_create_player_with_empty_username(self):
        message_bus = bootstrap_test_message_bus()

        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreatePlayer(username="")
        )

        with pytest.raises(exceptions.InvalidPlayerUsername):
            async_result.get()  # Wait for result
