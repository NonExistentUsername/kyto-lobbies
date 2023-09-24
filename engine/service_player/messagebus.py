from __future__ import annotations

import logging
import multiprocessing.pool
from typing import TYPE_CHECKING, Any, Callable, List, Union

from domain import commands, events
from service_player import exceptions

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: dict[events.Event, list[Callable]],
        command_handlers: dict[commands.Command, Callable],
        background_threads: int = 1,
    ):
        self.uow: unit_of_work.AbstractUnitOfWork = uow
        self.event_handlers: dict[events.Event, list[Callable]] = event_handlers
        self.command_handlers: dict[commands.Command, Callable] = command_handlers
        self.pool = multiprocessing.pool.ThreadPool(background_threads)

    def handle(self, message: Message) -> multiprocessing.pool.AsyncResult:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """
        return self.pool.apply_async(self._handle, (message,))

    def _collect_new_events(self) -> None:
        for event in self.uow.collect_new_events():
            self.handle(event)

    def _handle(self, message: Message) -> Any:
        result = None
        for handler in self._get_handlers(message):
            result = handler(message)

        self.pool.apply_async(self._collect_new_events)

        if isinstance(message, commands.Command):
            return result

    def _get_handlers(self, message: Message) -> list[Callable]:
        if isinstance(message, commands.Command):
            return self._get_command_handlers(message)
        elif isinstance(message, events.Event):
            return self._get_event_handlers(message)

        raise ValueError(f"Unexpected message {message}")

    def _get_command_handlers(self, command: commands.Command) -> List[Callable]:
        return [self.command_handlers[type(command)]]

    def _get_event_handlers(self, event: events.Event) -> List[Callable]:
        return self.event_handlers[type(event)]

    def _try_process(self, func: Callable) -> Any:
        try:
            return func()
        except exceptions.InternalException as e:
            logger.debug(
                f"Exception processing {func}"
            )  # Do not log stacktrace, because it is expected
            return e
        except Exception as e:
            logger.exception(f"Exception processing {func}")
            return e
