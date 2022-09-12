from ..mode.base import BaseModeSingleEffect


class EventMode(BaseModeSingleEffect):
    """Event makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/event"

    def __init__(self, effect_image_path: str, use_filter_points: bool = True) -> None:
        super().__init__(effect_image_path, use_filter_points=use_filter_points)
