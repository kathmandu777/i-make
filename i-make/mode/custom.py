from ..mode.base import BaseModeMultiEffects


class CustomMode(BaseModeMultiEffects):
    """Custom makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/custom"

    def __init__(self, effect_image_path: list[str], use_filter_points: bool = True) -> None:
        super().__init__(effect_image_path, use_filter_points=use_filter_points)
