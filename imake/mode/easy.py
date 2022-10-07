from typing import Any

from ..mode.base import BaseModeEffect


class EasyMode(BaseModeEffect):
    """Easy makeup mode."""

    MAKEUP_IMAGES_DIR_PATH = "imake/static/modes/easy"
    THUMBNAILS_DIR_PATH = "imake/static/modes/easy/thumbnails"

    ICON_PATH: str = "imake/static/modes/easy/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/modes/easy/menu.jpg"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
