from __future__ import annotations

import abc

from adapters import AbstractRepository, RamRepository


class AbstractUnitOfWork(abc.ABC):
    players: AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        """
        Commit all changes made in this unit of work
        """
        self._commit()

    def collect_new_events(self):
        """
        Collect all new events from all instances in the repository

        Yields:
            Event: New event
        """
        for instance in self.players.seen:
            if hasattr(instance, "events") and isinstance(instance.events, list):
                while instance.events:
                    yield instance.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        """
        Rollback all changes made in this unit of work

        Raises:
            NotImplementedError: Not implemented
        """
        raise NotImplementedError


class RamUnitOfWork(AbstractUnitOfWork):
    def __init__(self, players: RamRepository):
        self.players: RamRepository = players
        self.players_history: list[RamRepository] = [self.players]

    def _commit(self):
        self.players_history.append(self.repository.copy())

    def rollback(self):
        if len(self.players_history) > 1:
            self.repository = self.players_history.pop()

        if len(self.players_history) == 1:
            self.repository = self.players_history[0]
