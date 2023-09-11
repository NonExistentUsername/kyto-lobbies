from __future__ import annotations

import abc
from typing import Generic, Optional, TypeVar

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


class RamPlayerRepository(AbstractRepository[players.Player]):
    def __init__(
        self,
        storage_by_id: Optional[dict[str, players.Player]] = None,
        storage_by_username: Optional[dict[str, players.Player]] = None,
    ):
        super().__init__()
        self._storage_by_id: dict[str, players.Player] = storage_by_id or {}
        self._storage_by_username: dict[str, players.Player] = storage_by_username or {}

    def copy(self) -> RamPlayerRepository:
        """
        Copy repository

        Returns:
            RamRepository: Copy of repository
        """
        storage_by_id = self._storage_by_id.copy()
        storage_by_username = self._storage_by_username.copy()
        repository = RamPlayerRepository(storage_by_id, storage_by_username)
        repository.seen = self.seen.copy()
        return repository

    def __len__(self) -> int:  # For testing purposes
        return len(self._storage_by_id)

    def _add(self, instance: players.Player) -> None:
        self._storage_by_id[instance.id] = instance
        self._storage_by_username[instance.username] = instance

    def _get(self, **kwargs) -> Optional[players.Player]:
        if id := kwargs.get("id", None):
            return self._storage_by_id.get(id, None)

        username: Optional[str] = kwargs.get("username", None)
        return self._storage_by_username.get(username, None) if username else None
