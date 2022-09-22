from ..mode.base import BaseModeEffect


class EventMode(BaseModeEffect):
    """Event makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/event"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
