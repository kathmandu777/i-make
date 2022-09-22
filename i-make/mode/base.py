import os

import cv2
import numpy as np
from PIL import Image

from ..libs.effect import Effect


class BaseMode:
    """Base class for all modes."""

    ICON_PATH: str = ""
    DESCRIPTION: str = ""


class BaseModeEffect(BaseMode, Effect):
    """Base class for all modes that use Effect."""

    # Path to the directory containing the images for the choices. Must be overridden.
    CHOICE_IMAGES_DIR_PATH: str = ""
    SKIN_IMAGE_PATH: str = "i-make/static/facepaints/custom/skin/skin0.png"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_effect_image_from_path(self, effect_image_path: list[str] | str) -> None:
        """Set effect image from path.

        Args:
            effect_image_path (_type_): path to effect image
        """

        if isinstance(effect_image_path, str):
            effect_image_path = [effect_image_path]
        self.effect_image_paths = effect_image_path
        self.set_effect_image(self._overlay_effect_images())

    def _overlay_effect_images(self):
        """Overlay effect images.

        Returns:
            _type_: effect image for EffectCreator
        """

        effect_image = cv2.imread(self.SKIN_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
        for image_path in self.effect_image_paths:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            if not (image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT and image.shape[1] == Effect.EFFECT_IMAGE_WIDTH):
                raise ValueError("Effect image size must be 1024x1024")
            effect_image = self._overlay_alpha_image(effect_image, image)
        return effect_image

    def _overlay_alpha_image(self, back, front):
        """Overlay alpha image on the background image.

        Args:
            back (_type_): background image (RGBA)
            front (_type_): front image (RGBA). The size must be the same as the background image.

        Returns:
            _type_: overlayed image
        """

        back_pil = Image.fromarray(back)
        front_pil = Image.fromarray(front)
        image = Image.alpha_composite(back_pil, front_pil)
        return np.array(image).astype(np.uint8)

    def set_skin_color(self, color):
        """Set skin color.

        Args:
            color (_type_):

        Returns:
            _type_: _description_
        """
        # TODO: ゴルゴが実装した色の変換コード
        return

    @classmethod
    def get_choice_images_paths(cls):
        """Get the paths to the images for the choices."""
        return [
            os.path.join(cls.CHOICE_IMAGES_DIR_PATH, file)
            for file in os.listdir(cls.CHOICE_IMAGES_DIR_PATH)
            if file.endswith(".png")
        ]
