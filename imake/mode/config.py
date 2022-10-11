from typing import Any

from ..mode.base import BaseModeEffect


class ConfigMode(BaseModeEffect):
    """Config mode."""

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
