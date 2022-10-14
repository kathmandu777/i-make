import os

from pydantic import Field
from pydantic.dataclasses import dataclass

from .color import HSV


@dataclass
class FacePaint:
    filename: str = Field(
        ...,
    )
    image_dir_path: str = Field(...)
    thumbnail_dir_path: str | None = None
    hsv: HSV | None = None

    # custom
    part_name: str | None = None

    @property
    def image_path(self) -> str:
        return os.path.join(self.image_dir_path, self.filename)

    @property
    def thumbnail_path(self) -> str | None:
        if self.thumbnail_dir_path is None:
            return None
        if os.path.isfile(
            os.path.join(self.thumbnail_dir_path, self.filename).replace(".png", "").replace(".PNG", "") + ".png"
        ):
            return (
                os.path.join(self.thumbnail_dir_path, self.filename).replace(".png", "").replace(".PNG", "") + ".png"
            )
        elif os.path.isfile(
            os.path.join(self.thumbnail_dir_path, self.filename).replace(".png", "").replace(".PNG", "") + ".PNG"
        ):
            return (
                os.path.join(self.thumbnail_dir_path, self.filename).replace(".png", "").replace(".PNG", "") + ".PNG"
            )
        else:
            return None

    @property
    def image_path_for_frontend(self) -> str:
        return "../" + self.image_path.replace("imake/static/", "")

    @property
    def thumbnail_path_for_frontend(self) -> str:
        return (
            "../" + self.thumbnail_path.replace("imake/static/", "")
            if self.thumbnail_path
            else self.image_path_for_frontend
        )
