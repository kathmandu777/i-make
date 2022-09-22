from ..mode.base import BaseModeEffect


class PracticeMode(BaseModeEffect):
    """Practice makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/practice"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
