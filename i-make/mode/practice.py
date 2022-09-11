from ..mode.base import BaseModeSingleEffect


class PracticeMode(BaseModeSingleEffect):
    """Practice makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/practice"

    def __init__(self, effect_image_path: str, use_filter_points: bool = True) -> None:
        super().__init__(effect_image_path, use_filter_points=use_filter_points)
