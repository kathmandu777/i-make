from typing import Any

from ..mode.base import BaseModeEffect


class ConfigMode(BaseModeEffect):
    """Config mode."""

    ADJUSTMENT_IMAGE_PATH = "imake/static/modes/config/sample.png"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
