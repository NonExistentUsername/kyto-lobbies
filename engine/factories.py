from typing import Callable, List, Literal

import di
from adapters import repository
from domain import commands, events
from service_player import handlers, messagebus, unit_of_work


def create_repository(
    type: Literal["ram", "sql"]
) -> repository.AbstractPlayerRepository:
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
        return repository.RamPlayerRepository()

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


def create_message_bus(
    uow: unit_of_work.AbstractUnitOfWork,
    event_handlers: dict[events.Event, List[Callable]] = handlers.EVENT_HANDLERS,
    command_handlers: dict[commands.Command, Callable] = handlers.COMMAND_HANDLERS,
) -> messagebus.MessageBus:
    """
    Create message bus

    Args:
        uow (unit_of_work.AbstractUnitOfWork): Unit of work

    Returns:
        messagebus.MessageBus: Message bus
    """

    dependencies = {
        "uow": uow,
    }

    injected_command_handlers = {
        command: di.inject_dependencies(handler, dependencies)
        for command, handler in command_handlers.items()
    }
    injected_event_handlers = {
        event: [
            di.inject_dependencies(handler, dependencies) for handler in handlers_list
        ]
        for event, handlers_list in event_handlers.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
