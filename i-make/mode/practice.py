from ..mode.base import BaseModeEffect


class PracticeMode(BaseModeEffect):
    """Practice makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/practice"
    THUMBNAIL_IMAGES_DIR_PATH = "i-make/static/facepaints/practice/thumbnails"

    ICON_PATH: str = "i-make/static/facepaints/practice/icon.png"
    MENU_IMAGE_PATH: str = "i-make/static/facepaints/practice/menu.png"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
