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
        self._commit()

    def collect_new_events(self):
        for instance in self.repository.seen:
            while instance.events:
                yield instance.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
