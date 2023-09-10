from typing import Literal

from adapters import repository
from service_player import messagebus, unit_of_work


def create_repository(type: Literal["ram", "sql"]) -> repository.AbstractRepository:
    """
    Create repository

    Args:
        type (Literal["ram", "sql"]): Type of repository

    Raises:
        NotImplementedError: If type is not implemented
        ValueError: If type is unknown

    Returns:
        unit_of_work.AbstractRepository: Repository
    """
    if type == "ram":
        return repository.RamRepository()

    elif type == "sql":
        raise NotImplementedError

    raise ValueError("Unknown type of repository")


def create_uow(type: Literal["ram", "sql"]) -> unit_of_work.AbstractUnitOfWork:
    """
    Create unit of work

    Args:
        type (Literal["ram", "sql"]): Type of unit of work

    Raises:
        NotImplementedError: If type is not implemented
        ValueError: If type is unknown

    Returns:
        unit_of_work.AbstractUnitOfWork: Unit of work
    """
    if type == "ram":
        return unit_of_work.RamUnitOfWork(create_repository("ram"))

    elif type == "sql":
        raise NotImplementedError

    raise ValueError("Unknown type of unit of work")


def create_message_bus() -> messagebus.MessageBus:
    return messagebus.MessageBus(
        create_uow("ram"),
    )
