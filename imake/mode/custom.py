import os
from dataclasses import asdict
from typing import Any

from ..dataclasses import FacePaint
from ..mode.base import BaseModeEffect


class CustomMode(BaseModeEffect):
    """Custom makeup mode."""

    MAKEUP_IMAGES_DIR_PATH = "imake/static/facepaints/custom"
    ICON_PATH: str = "imake/static/facepaints/custom/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/facepaints/custom/menu.png"

    THUMBNAIL_IMAGE_NAME = "thumbnail.png"
    THUMBNAIL_DIR_NAME = "thumbnails"

    IGNORE_DIRS = ["skin"]

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def get_choice_facepaints_by_part(cls, part_kind: str) -> list[dict]:
        """選択肢のメイクを取得する.

        Returns:
            list[FacePaint]: メイクのリスト
        """
        if not (part_kind in [x["part_kind"] for x in cls.get_part_kinds()]):
            raise ValueError(f"part_kind must be in {[x['part_kind'] for x in cls.get_part_kinds()]}, but {part_kind}")

        facepaints = [
            FacePaint(
                filename=file,
                image_dir_path=os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_kind),
                thumbnail_dir_path=os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_kind, cls.THUMBNAIL_DIR_NAME),
                part_kind=part_kind,
            )
            for file in os.listdir(os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_kind))
            if file.endswith(".png") and not file == cls.THUMBNAIL_IMAGE_NAME and not (cls.BASE_IMAGE_SUFFIX in file)
        ]
        return [
            {
                **asdict(facepaint),
                "thumbnail_path_for_frontend": facepaint.thumbnail_path_for_frontend,
                "image_path": facepaint.image_path,
            }
            for facepaint in facepaints
        ]

    @classmethod
    def get_part_kinds(cls) -> list[dict]:
        """パーツの種類を取得する.

        Returns:
            list[str]: パーツの種類のリスト
        """
        return [
            dict(
                part_kind=dirname,
                thumbnail_path_for_frontend="../"
                + os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, dirname, cls.THUMBNAIL_IMAGE_NAME).replace(
                    "imake/static/", ""
                ),
            )
            for dirname in os.listdir(cls.MAKEUP_IMAGES_DIR_PATH)
            if not dirname.endswith(".png") and not dirname.startswith(".") and dirname not in cls.IGNORE_DIRS
        ]
