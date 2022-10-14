import os
from dataclasses import asdict
from typing import Any, Final

from ..dataclasses import FacePaint
from ..libs.list import get_index
from ..libs.palette import PALETTE
from ..mode.base import BaseModeEffect


class CustomMode(BaseModeEffect):
    """Custom makeup mode."""

    ICON_PATH: str = "imake/static/modes/custom/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/modes/custom/menu.png"

    MAKEUP_IMAGES_DIR_PATH: str = "imake/static/modes/custom"

    THUMBNAIL_IMAGE_NAME: Final = "thumbnail.png"
    THUMBNAIL_DIR_NAME: Final = "thumbnails"

    IGNORE_DIRS: Final = ["skin"]

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def get_choice_facepaints_by_part_name(cls, part_name: str) -> list[dict]:
        """選択肢のメイクを取得する.

        Returns:
            list[dict]: メイクのリスト
        """
        if not (part_name in [x["name"] for x in cls.get_parts()]):
            raise ValueError(f"part_name must be in {[x['name'] for x in cls.get_parts()]}, but {part_name}")

        order = cls.get_order(os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_name))

        choice_files = [
            file
            for file in os.listdir(os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_name))
            if (file.endswith(".png") or file.endswith(".PNG"))
            and not file == cls.THUMBNAIL_IMAGE_NAME
            and not (cls.BASE_IMAGE_SUFFIX in file)
        ]
        facepaints = [
            FacePaint(
                filename=file,
                image_dir_path=os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_name),
                thumbnail_dir_path=os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_name, cls.THUMBNAIL_DIR_NAME),
                part_name=part_name,
            )
            for file in sorted(choice_files, key=lambda x: get_index(order, x, cls.DEFAULT_ORDER))
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
    def get_palette_by_part_name(cls, part_name: str) -> list[dict]:
        """Get color palette by part name.

        Args:
            part_name (str): 顔のパーツ名

        Returns:
            _type_: HSVのリスト
        """
        if not (part_name in [x["name"] for x in cls.get_parts()]):
            raise ValueError(f"part_name must be in {[x['name'] for x in cls.get_parts()]}, but {part_name}")

        palette_name = cls.get_palette_name(os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part_name))
        return [asdict(hsv) for hsv in PALETTE.get(palette_name, [])]

    @classmethod
    def get_parts(cls) -> list[dict]:
        """パーツの種類を取得する.

        Returns:
            list[str]: パーツの種類のリスト
        """
        order = cls.get_order(cls.MAKEUP_IMAGES_DIR_PATH)

        part_choices = [
            dirname
            for dirname in os.listdir(cls.MAKEUP_IMAGES_DIR_PATH)
            if not dirname.startswith(".")
            and dirname not in cls.IGNORE_DIRS
            and os.path.isdir(os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, dirname))
        ]
        return [
            dict(
                name=part,
                thumbnail_path_for_frontend="../"
                + os.path.join(cls.MAKEUP_IMAGES_DIR_PATH, part, cls.THUMBNAIL_IMAGE_NAME).replace(
                    "imake/static/", ""
                ),
            )
            for part in sorted(part_choices, key=lambda x: get_index(order, x, cls.DEFAULT_ORDER))
        ]
