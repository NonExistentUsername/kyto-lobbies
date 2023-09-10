import abc
from typing import Generic, Optional, TypeVar

_T = TypeVar("_T")


class AbstractRepository(abc.ABC, Generic[_T]):
    def __init__(self):
        self.seen: set[_T] = set()

    def add(self, instance: _T) -> None:
        self._add(instance)
        self.seen.add(instance)

    def get(self, id: str) -> Optional[_T]:
        instance: _T = self._get(id)
        if instance:
            self.seen.add(instance)
        return instance

    @abc.abstractmethod
    def _add(self, instance: _T) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: str) -> Optional[_T]:
        raise NotImplementedError


class RamRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.seen: set[_T] = set()
        self._storage: dict[str, _T] = {}

    def _add(self, instance: _T) -> None:
        self._storage[instance.id] = instance

    def _get(self, id: str) -> Optional[_T]:
        return self._storage.get(id, None)
