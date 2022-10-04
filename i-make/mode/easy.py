from ..mode.base import BaseModeEffect


class EasyMode(BaseModeEffect):
    """Easy makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/easy"
    THUMBNAIL_IMAGES_DIR_PATH = "i-make/static/facepaints/easy/thumbnails"

    ICON_PATH: str = "i-make/static/facepaints/easy/icon.png"
    MENU_IMAGE_PATH: str = "i-make/static/facepaints/easy/menu.png"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
