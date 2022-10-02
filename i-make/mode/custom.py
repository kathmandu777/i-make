import os
from dataclasses import asdict

from ..dataclasses import FacePaint
from ..mode.base import BaseModeEffect


class CustomMode(BaseModeEffect):
    """Custom makeup mode."""

    CHOICE_IMAGES_DIR_PATH = "i-make/static/facepaints/custom"
    ICON_PATH: str = "i-make/static/facepaints/custom/costom.png"

    IGNORE_DIRS = ["skin"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def get_choice_facepaints(cls) -> list[dict]:
        """選択肢のメイクを取得する.

        Returns:
            list[FacePaint]: メイクのリスト
        """
        dirs = [
            dir_file
            for dir_file in os.listdir(cls.CHOICE_IMAGES_DIR_PATH)
            if not dir_file.endswith(".png") and not dir_file.startswith(".") and dir_file not in cls.IGNORE_DIRS
        ]
        facepaints = [
            FacePaint(
                filename=file,
                image_dir_path=os.path.join(cls.CHOICE_IMAGES_DIR_PATH, dir),
                thumbnail_dir_path=cls.THUMBNAIL_IMAGES_DIR_PATH,
                dir=dir,
            )
            for dir in dirs
            for file in os.listdir(os.path.join(cls.CHOICE_IMAGES_DIR_PATH, dir))
            if file.endswith(".png")
        ]
        return [
            {
                **asdict(facepaint),
                "thumbnail_path_for_frontend": facepaint.thumbnail_path_for_frontend,
                "image_path": facepaint.image_path,
            }
            for facepaint in facepaints
        ]
