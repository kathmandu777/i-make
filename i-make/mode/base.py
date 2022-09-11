import os

import cv2
import numpy as np
from PIL import Image

from ..libs.effect import Effect


class BaseMode:
    """Base class for all modes."""

    # Path to the directory containing the images for the choices. Must be overridden.
    CHOICE_IMAGES_DIR_PATH: str = ""

    @classmethod
    def show_choice_images(cls):
        """Show the images for the choices."""
        for file in os.listdir(cls.CHOICE_IMAGES_DIR_PATH):
            if file.endswith(".png"):
                print(file)

    @classmethod
    def get_choice_images_paths(cls):
        """Get the paths to the images for the choices."""
        return [
            os.path.join(cls.CHOICE_IMAGES_DIR_PATH, file)
            for file in os.listdir(cls.CHOICE_IMAGES_DIR_PATH)
            if file.endswith(".png")
        ]


class BaseModeSingleEffect(BaseMode, Effect):
    """Base class for modes with a single effect image."""

    def __init__(self, effect_image_path: str, use_filter_points: bool = True) -> None:
        self.effect_image_path = effect_image_path
        effect_image = cv2.imread(effect_image_path, cv2.IMREAD_UNCHANGED)
        if effect_image is None:
            raise ValueError(f"Failed to read image: {effect_image_path}")

        super().__init__(effect_image, use_filter_points=use_filter_points)


class BaseModeMultiEffects(BaseMode, Effect):
    """Base class for modes with multiple effect images."""

    def __init__(self, effect_image_paths: list[str], use_filter_points: bool = True) -> None:
        self.effect_image_paths = effect_image_paths
        effect_image = self.overlay_effect_images()
        super().__init__(effect_image, use_filter_points=use_filter_points)

    def overlay_effect_images(self):
        """Overlay effect images.

        Returns:
            _type_: effect image for EffectCreator
        """

        effect_image = np.zeros((Effect.EFFECT_IMAGE_HEIGHT, Effect.EFFECT_IMAGE_WIDTH, 4), dtype=np.uint8)
        for image_path in self.effect_image_paths:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            if not (image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT and image.shape[1] == Effect.EFFECT_IMAGE_WIDTH):
                raise ValueError("Effect image size must be 1024x1024")
            effect_image = self.overlay_alpha_image(effect_image, image)
        return effect_image

    def overlay_alpha_image(self, back, front):
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
