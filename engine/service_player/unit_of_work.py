from __future__ import annotations

import abc

from adapters import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    repository: AbstractRepository

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
        for instance in self.repository.seen:
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

