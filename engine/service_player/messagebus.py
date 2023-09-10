from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Union

from domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: dict[events.Event, list[callable]],
        command_handlers: dict[commands.Command, callable],
    ):
        self.uow: unit_of_work.AbstractUnitOfWork = uow
        self.event_handlers: dict[events.Event, list[callable]] = event_handlers
        self.command_handlers: dict[commands.Command, callable] = command_handlers

    def handle(self, message: Message) -> None:
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

    def _handle_event(self, event: events.Event) -> None:
        """
        Handle event

        Args:
            event (events.Event): Event to handle
        """
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with handler {handler}")

                handler(event)  # Handle event

                self.queue.extend(self.uow.collect_new_events())  # Collect new events
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    def _handle_command(self, command: commands.Command) -> None:
        """
        Handle command

        Args:
            command (commands.Command): Command to handle
        """
        logger.debug(f"Handling command {command}")
        try:
            handler = self.command_handlers[type(command)]  # Get handler

            handler(command)  # Handle command

            self.queue.extend(self.uow.collect_new_events())  # Collect new events
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise
