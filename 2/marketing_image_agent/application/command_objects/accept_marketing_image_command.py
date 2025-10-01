from typing import Dict, Any
from .base_command_object import Command


class AcceptMarketingImageCommand(Command):
    def __init__(
        self,
        data: Dict[str, Any],
        source: str,
        command_prefix: str,
        version: str = "1.0",
    ):
        super().__init__(
            type=f"{command_prefix}.accept",
            data=data,
            source=source,
            version=version,
        )
