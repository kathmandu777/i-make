from typing import Any

from ..mode.base import BaseModeEffect


class PracticeMode(BaseModeEffect):
    """Practice makeup mode."""

    MAKEUP_IMAGES_DIR_PATH = "imake/static/modes/practice"
    THUMBNAILS_DIR_PATH = "imake/static/modes/practice/thumbnails"

    ICON_PATH: str = "imake/static/modes/practice/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/modes/practice/menu.jpg"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
