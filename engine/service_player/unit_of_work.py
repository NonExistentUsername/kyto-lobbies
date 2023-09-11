from __future__ import annotations

import abc
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adapters import repository

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(abc.ABC):
    players: repository.AbstractRepository
    rooms: repository.AbstractRepository

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
    def __init__(
        self,
        players: repository.RamPlayerRepository,
        rooms: repository.RamRoomRepository,
    ):
        self.players: repository.RamPlayerRepository = players
        self.rooms: repository.RamRoomRepository = rooms

        self.players_history: list[repository.RamPlayerRepository] = [self.players]
        self.rooms_history: list[repository.RamRoomRepository] = [self.rooms]

    def _commit(self):
        logger.debug("Commiting changes in RamUnitOfWork")

        self.players_history.append(self.players.copy())
        self.rooms_history.append(self.rooms.copy())

    def rollback(self):
        logger.debug("Rolling back changes in RamUnitOfWork")
        if len(self.players_history) > 1:
            self.players = self.players_history.pop()
            self.rooms = self.rooms_history.pop()

        if len(self.players_history) == 1:
            self.players = self.players_history[0]
            self.rooms = self.rooms_history[0]
