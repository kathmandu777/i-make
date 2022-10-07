from typing import Any

from ..mode.base import BaseModeEffect


class EventMode(BaseModeEffect):
    """Event makeup mode."""

    MAKEUP_IMAGES_DIR_PATH = "imake/static/modes/event"
    THUMBNAILS_DIR_PATH = "imake/static/modes/event/thumbnails"

    ICON_PATH: str = "imake/static/modes/event/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/modes/event/menu.jpg"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
