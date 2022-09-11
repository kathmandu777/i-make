import cv2
import numpy as np
from PIL import Image

from .effect import EffectRenderer2D


class Makeup(EffectRenderer2D):
    def __init__(self, makeup_image_paths: list[str], use_filter_points: bool, **kwargs):
        """Initialize Makeup.

        Args:
            makeup_image_paths (list[str]): makeup image paths. リストの先頭から順にメイクを重ねていく
            use_filter_points (bool): use filter landmarks
            **kwargs: keyword arguments for EffectRenderer2D
        """

        effect_image = np.zeros((self.EFFECT_IMAGE_HEIGHT, self.EFFECT_IMAGE_WIDTH, 4), dtype=np.uint8)
        for image_path in makeup_image_paths:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            if not (image.shape[0] == self.EFFECT_IMAGE_HEIGHT and image.shape[1] == self.EFFECT_IMAGE_WIDTH):
                raise ValueError("Effect image size must be 1024x1024")
            effect_image = self.overlay_alpha_image(effect_image, image)
        super().__init__(effect_image, use_filter_points=use_filter_points, **kwargs)

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

    def convert_rgba_to_rgb(self, image):
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image

        Returns:
            _type_: RGB image
        """
        mask = image[:, :, 3]
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)
