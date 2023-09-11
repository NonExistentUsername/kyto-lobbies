from __future__ import annotations

import abc
from copy import deepcopy
from typing import Generic, List, Optional, TypeVar

from domain import players
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

    def get(self, **kwargs) -> Optional[_T]:
        """
        Get instance from repository by keyword arguments

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """
        instance: Optional[_T] = self._get(**kwargs)

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
    def _get(self, **kwargs) -> Optional[_T]:
        """
        Get instance from repository by keyword arguments

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """
        raise NotImplementedError


class RamRepository(AbstractRepository[_T]):
    def __init__(
        self,
        fields: Optional[List[str]] = None,
        storages: Optional[dict[str, dict[str, _T]]] = None,
    ):
        super().__init__()
        self._fields: List[str] = fields or []
        self._storages: dict[str, dict[str, _T]] = storages or {}

        for field in self._fields:
            if field not in self._storages:
                self._storages[field] = {}

    def copy(self) -> RamRepository[_T]:
        """
        Copy repository

        Returns:
            RamRepository: Copy of repository
        """
        fields = self._fields.copy()
        storages = deepcopy(self._storages)
        repository = RamRepository(fields, storages)
        repository.seen = self.seen.copy()
        return repository

    def __len__(self) -> int:  # For testing purposes
        return len(self._storages[self._fields[0]])

    def _add(self, instance: _T) -> None:
        for field in self._fields:
            value = getattr(instance, field)
            self._storages[field][value] = instance

    def _get(self, **kwargs) -> Optional[players.Player]:
        for field in self._fields:
            if value := kwargs.get(field, None):
                return self._storages[field].get(value, None)

        return None


class RamPlayerRepository(RamRepository[players.Player]):
    def __init__(
        self,
        fields: Optional[List[str]] = None,
        storages: Optional[dict[str, dict[str, players.Player]]] = None,
    ):
        fields = fields or ["id", "username"]
        super().__init__(fields, storages)
