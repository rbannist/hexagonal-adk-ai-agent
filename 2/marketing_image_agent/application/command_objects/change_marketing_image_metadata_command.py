from typing import Dict, Any
from .base_command_object import Command


class ChangeMarketingImageMetadataCommand(Command):
    def __init__(
        self,
        data: Dict[str, Any],
        source: str,
        command_prefix: str,
        version: str = "1.0",
        **kwargs,
    ):
        super().__init__(
            type=f"{command_prefix}.change-metadata",
            data=data,
            source=source,
            version=version,
        )
