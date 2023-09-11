import contextlib

import factories
from domain import players


class TestRamUOWCreation:
    def test_works(self):
        uow = factories.create_uow("ram")

        with uow:
            uow.players.add(players.Player(id="123", username="test"))
            uow.commit()

        assert uow.players.get(username="test") is not None

    def test_rolls_back(self):
        uow = factories.create_uow("ram")

        with uow:
            uow.players.add(players.Player(id="123", username="test"))

        assert uow.players.get(username="test") is None

    def test_rolls_back_if_exception(self):
        uow = factories.create_uow("ram")

        with contextlib.suppress(ValueError):
            with uow:
                uow.players.add(players.Player(id="123", username="test"))
                raise ValueError("oops")

        assert uow.players.get(username="test") is None

        with contextlib.suppress(ValueError):
            with uow:
                with uow:
                    with uow:
                        uow.players.add(players.Player(id="123", username="test"))
                        raise ValueError("oops")

        assert uow.players.get(username="test") is None
