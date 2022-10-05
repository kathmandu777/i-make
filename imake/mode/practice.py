from typing import Any

from ..mode.base import BaseModeEffect


class PracticeMode(BaseModeEffect):
    """Practice makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "imake/static/facepaints/practice"
    THUMBNAIL_IMAGES_DIR_PATH = "imake/static/facepaints/practice/thumbnails"

    ICON_PATH: str = "imake/static/facepaints/practice/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/facepaints/practice/menu.png"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
