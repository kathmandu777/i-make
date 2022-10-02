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
    dir: str | None = None

    @property
    def image_path(self) -> str:
        return os.path.join(self.image_dir_path, self.filename)

    @property
    def thumbnail_path(self) -> str | None:
        return (
            os.path.join(self.thumbnail_dir_path, self.filename)
            if self.thumbnail_dir_path and os.path.isfile(os.path.join(self.thumbnail_dir_path, self.filename))
            else None
        )

    @property
    def image_path_for_frontend(self) -> str:
        return "../" + self.image_path.replace("i-make/static/", "")

    @property
    def thumbnail_path_for_frontend(self) -> str:
        return (
            "../" + self.thumbnail_path.replace("i-make/static/", "")
            if self.thumbnail_path
            else self.image_path_for_frontend
        )
