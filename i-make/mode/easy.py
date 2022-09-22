from ..mode.base import BaseModeEffect


class EasyMode(BaseModeEffect):
    """Easy makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/otegaru"  # TODO: otegaru -> easy

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)