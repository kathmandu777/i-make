from typing import Any

from ..mode.base import BaseModeEffect


class EasyMode(BaseModeEffect):
    """Easy makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "imake/static/facepaints/easy"
    THUMBNAIL_IMAGES_DIR_PATH = "imake/static/facepaints/easy/thumbnails"

    ICON_PATH: str = "imake/static/facepaints/easy/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/facepaints/easy/menu.png"

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)
