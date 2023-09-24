from __future__ import annotations

import abc
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from domain import commands, events
from service_player import exceptions

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]
MessageResult = Union[commands.CommandResult, None]


class ResultDispatcher:  # Created for dispatching results to future results
    def __init__(self):
        self.__listeners: Dict[str, Callable] = {}

    def add_listener(self, message_id: str, listener: Callable) -> None:
        self.__listeners[message_id] = listener

    def remove_listener(self, message_id: str) -> None:
        self.__listeners.pop(message_id)

    def dispatch(self, result: MessageResult) -> None:
        if result is None:
            return

        if isinstance(result, commands.CommandResult):
            self.__dispatch_command_result(result)
        else:
            raise ValueError(f"Unexpected result {result}")

    def __dispatch_command_result(self, result: commands.CommandResult) -> None:
        if result.command.id in self.__listeners:
            self.__listeners[result.command.id](result)
            self.remove_listener(result.command.id)


class FutureResult:
    def __init__(self):
        self._result = None
        self._is_set = False

    def get_handler(self) -> Callable:
        def handler(result: Any) -> None:
            self._result = result
            self._is_set = True

        return handler

    def await_result(self) -> MessageResult:
        while not self.is_set:
            import time

            time.sleep(0.01)  # TODO: Replace with asyncio.sleep

        if isinstance(self.result, Exception):
            raise self.result

        return self.result

    @property
    def is_set(self) -> bool:
        return self._is_set

    @property
    def result(self) -> Any:
        return self._result


def protect_result_decorator(func: Callable) -> Callable:
    def wrapper(message: Message) -> MessageResult:
        try:
            return func(message)
        except exceptions.InternalException as e:
            logger.debug(
                f"Exception processing {func}"
            )  # Do not log stacktrace, because it is expected
            return e
        except Exception as e:
            logger.exception(f"Exception processing {func}")
            return e

    return wrapper


def result_converter_decorator(func: Callable) -> Callable:
    def wrapper(message: Message) -> MessageResult:
        result = func(message)
        if isinstance(message, commands.Command):
            print(f"Result of {message} is {result}")
            return commands.CommandResult(command=message, result=result)
        return None

    return wrapper


class IMessageBus:
    @abc.abstractmethod
    def handle(self, message: Message) -> Optional[FutureResult]:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """
        raise NotImplementedError


class MessageBus(IMessageBus):
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: dict[events.Event, list[Callable]],
        command_handlers: dict[commands.Command, Callable],
    ):
        self.result_dispatcher = ResultDispatcher()
        self.uow: unit_of_work.AbstractUnitOfWork = uow
        self.event_handlers: dict[events.Event, list[Callable]] = event_handlers
        self.command_handlers: dict[commands.Command, Callable] = command_handlers

    def handle(self, message: Message) -> Optional[FutureResult]:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """
        result = None

        if isinstance(message, commands.Command):
            result = FutureResult()
            self.result_dispatcher.add_listener(message.id, result.get_handler())

        self._run_queue(message)

        return result

    def _run_queue(self, message: Message) -> None:
        queue = [message]  # Create queue with message

        while queue:  # While queue is not empty
            self._handle(queue.pop(0))  # Handle message

            queue.extend(self._collect_new_events())  # Add new events to queue

    def _collect_new_events(self) -> List[Message]:
        return self.uow.collect_new_events()

    def _handle(self, message: Message) -> None:
        for handler in self._get_handlers(message):
            result = result_converter_decorator(protect_result_decorator(handler))(
                message
            )
            self.result_dispatcher.dispatch(result)

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
