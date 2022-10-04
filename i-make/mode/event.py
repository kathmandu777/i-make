from ..mode.base import BaseModeEffect


class EventMode(BaseModeEffect):
    """Event makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/event"
    THUMBNAIL_IMAGES_DIR_PATH = "i-make/static/facepaints/event/thumbnails"

    ICON_PATH: str = "i-make/static/facepaints/event/icon.png"
    MENU_IMAGE_PATH: str = "i-make/static/facepaints/event/menu.png"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
