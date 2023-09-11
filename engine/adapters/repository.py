import abc
from typing import Generic, Optional, TypeVar

from domain.base import BaseModel

_T = TypeVar("_T", bound=BaseModel)


class AbstractPlayerRepository(abc.ABC, Generic[_T]):
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

    def get(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Optional[_T]:
        """
        Get instance from repository

        Args:
            id (str): ID of instance

        Returns:
            Optional[_T]: Instance or None if not found
        """
        instance: Optional[_T] = self._get(id, username)
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
    def _get(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Optional[_T]:
        """
        Get instance from repository

        Args:
            id (Optional[str], optional): ID of instance. Defaults to None.
            username (Optional[str], optional): Username of instance. Defaults to None.

        Raises:
            NotImplementedError: _description_

        Returns:
            Optional[_T]: _description_
        """
        raise NotImplementedError


class RamRepository(AbstractPlayerRepository):
    def __init__(
        self,
        storage_by_id: Optional[dict[str, _T]] = None,
        storage_by_username: Optional[dict[str, _T]] = None,
    ):
        super().__init__()
        self.seen: set[_T] = set()
        self._storage_by_id: dict[str, _T] = storage_by_id or {}
        self._storage_by_username: dict[str, _T] = storage_by_username or {}

    def copy(self) -> "RamRepository":
        """
        Copy repository

        Returns:
            RamRepository: Copy of repository
        """
        storage_by_id = self._storage_by_id.copy()
        storage_by_username = self._storage_by_username.copy()
        repository = RamRepository(storage_by_id, storage_by_username)
        repository.seen = self.seen.copy()
        return repository

    def __len__(self) -> int:  # For testing purposes
        return len(self._storage_by_id)

    def _add(self, instance: _T) -> None:
        self._storage_by_id[instance.id] = instance
        self._storage_by_username[instance.username] = instance

    def _get(
        self, id: Optional[str] = None, uuid: Optional[str] = None
    ) -> Optional[_T]:
        if id:
            return self._storage_by_id.get(id, None)
        return self._storage_by_username.get(uuid, None) if uuid else None
