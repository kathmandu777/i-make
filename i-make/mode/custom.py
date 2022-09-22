from ..mode.base import BaseModeEffect


class CustomMode(BaseModeEffect):
    """Custom makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/custom"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
