from typing import Dict, Type

from ....application.ports.command_output_port import CommandOutputPort
from ....application.ports.command_input_port import CommandInputPort
from ....application.command_objects.base_command_object import Command


class InMemoryCommandDispatcher(CommandOutputPort):
    def __init__(self):
        self._handlers: Dict[Type[Command], CommandInputPort] = {}

    def register(self, command_type: Type[Command], handler: CommandInputPort):
        self._handlers[command_type] = handler

    def dispatch(self, command: Command):
        handler = self._handlers.get(type(command))
        if handler:
            command_handler_response = handler.handle(command)
            return command_handler_response
        else:
            raise ValueError(f"No handler registered for command type: {type(command)}")