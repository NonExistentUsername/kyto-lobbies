import abc
from typing import Generic, Optional, TypeVar

from domain.base import BaseModel

_T = TypeVar("_T", bound=BaseModel)


class AbstractRepository(abc.ABC, Generic[_T]):
    def __init__(self):
        self.seen: set[_T] = set()

    def add(self, instance: _T) -> None:
        """
        Add instance to repository

        Args:
            instance (_T): Instance
        """
        self._add(instance)
        self.seen.add(instance)

    def get(self, id: str) -> Optional[_T]:
        """
        Get instance from repository

        Args:
            id (str): ID of instance

        Returns:
            Optional[_T]: Instance or None if not found
        """
        instance: _T = self._get(id)
        if instance:
            self.seen.add(instance)
        return instance

    @abc.abstractmethod
    def _add(self, instance: _T) -> None:
        """
        Add instance to repository

        Args:
            instance (_T): Instance

        Raises:
            NotImplementedError: Not implemented
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: str) -> Optional[_T]:
        """
        Get instance from repository

        Args:
            id (str): ID of instance

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """
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
