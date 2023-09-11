from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Union

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
    ):
        self.uow: unit_of_work.AbstractUnitOfWork = uow
        self.event_handlers: dict[events.Event, list[Callable]] = event_handlers
        self.command_handlers: dict[commands.Command, Callable] = command_handlers

    def handle(self, message: Message) -> commands.CommandResult | None:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """
        self.queue: list[Message] = [message]
        result: commands.CommandResult | None = None

        while self.queue:
            message = self.queue.pop(0)

            if isinstance(message, events.Event):
                self._handle_event(message)
            elif isinstance(message, commands.Command):
                command_execution_result = self._handle_command(message)
                if result is None:
                    result = commands.CommandResult(message, command_execution_result)
            else:
                raise ValueError(f"{message} was not an Event or Command")

        return result

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
            except exceptions.InternalException as e:
                logger.info(
                    f"Exception handling event {event}"
                )  # Do not log stacktrace, because it is expected
                raise e
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    def _handle_command(self, command: commands.Command) -> Any:
        """
        Handle command

        Args:
            command (commands.Command): Command to handle
        """
        logger.debug(f"Handling command {command}")

        try:
            handler = self.command_handlers[type(command)]  # Get handler

            result = handler(command)  # Handle command

            self.queue.extend(self.uow.collect_new_events())  # Collect new events

            return result  # Return command execution result
        except exceptions.InternalException as e:
            logger.info(
                f"Exception handling command {command}"
            )  # Do not log stacktrace, because it is expected
            raise e
        except Exception as e:
            logger.exception(f"Exception handling command {command}")
            raise e
