from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Dict, List, Type, Union

from domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """
        self.queue: list[Message] = [message]

        while self.queue:
            message: Message = self.queue.pop(0)

            if isinstance(message, events.Event):
                self._handle_event(message)
            elif isinstance(message, commands.Command):
                self._handle_command(message)
            else:
                raise ValueError(f"{message} was not an Event or Command")

    def _handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with handler {handler}")

                handler(event)  # Handle event

                self.queue.extend(self.uow.collect_new_events())  # Collect new events
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    def _handle_command(self, command: commands.Command):
        logger.debug(f"Handling command {command}")
        try:
            handler = self.command_handlers[type(command)]  # Get handler

            handler(command)  # Handle command

            self.queue.extend(self.uow.collect_new_events())  # Collect new events
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise
