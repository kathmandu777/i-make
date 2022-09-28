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
    SKIN_IMAGE_PATH: str = "i-make/static/facepaints/custom/skin/skin.png"

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

    def set_effect_image_from_path_w_hsv(
        self,
        effect_image_path: list[str] | str,
        effect_image_hsv: list[tuple[float, float, float]] | tuple[float, float, float],
    ) -> None:
        """Set effect image from path.

        Args:
            effect_image_path (_type_): path to effect image
            effect_image_hsv(_type_):HSV figures after change
        """

        if isinstance(effect_image_path, str):
            effect_image_path = [effect_image_path]

        if isinstance(effect_image_hsv, tuple):
            effect_image_hsv = [effect_image_hsv]

        if not (len(effect_image_path) == len(effect_image_hsv)):
            raise ValueError("The number of image paths and hsv paths do not match")

        self.effect_image_paths = effect_image_path
        self.effect_image_hsv_list = effect_image_hsv
        self.set_effect_image(self._overlay_effect_images_w_hsv())

    def _overlay_effect_images(self):
        """Overlay effect images on skin image.

        Returns:
            _type_: effect image for EffectCreator
        """
        if self.skin_image is None:
            raise ValueError("skin_image is None")

        effect_image = self.skin_image
        for image_path in self.effect_image_paths:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            if not (image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT and image.shape[1] == Effect.EFFECT_IMAGE_WIDTH):
                raise ValueError("Effect image size must be 1024x1024")
            effect_image = self._overlay_alpha_image(effect_image, image)
        return effect_image

    def _overlay_effect_images_w_hsv(self):
        """Overlay effect images on skin image.

        Returns:
            _type_: effect image for EffectCreator
        """
        if self.skin_image is None:
            raise ValueError("skin_image is None")

        effect_image = self.skin_image
        if len(self.effect_image_paths) == len(self.effect_image_hsv_list):
            for image_path, hsv_list in zip(self.effect_image_paths, self.effect_image_hsv_list):
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                if image is None:
                    raise ValueError(f"Failed to read image: {image_path}")
                if not (image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT and image.shape[1] == Effect.EFFECT_IMAGE_WIDTH):
                    raise ValueError("Effect image size must be 1024x1024")
                h, s, v = hsv_list
                image = self._convert_image_color(image, h, s, v, True)
                effect_image = self._overlay_alpha_image(effect_image, image)
            return effect_image
        else:
            raise ValueError("The number of image paths and hsv paths do not match")

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

    def set_skin_color(self, hue: float, sat: float, val: float) -> None:
        """指定したHSVにスキンカラーをセットする.

        Args:
            hue (float, optional): HSVのHueの数値
            sat (float, optional): HSVのSaturationの数値
            val (float, optional): HSVのVvalueの数値
        """
        base_skin_image = cv2.imread(self.SKIN_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
        if base_skin_image is None:
            raise ValueError(f"Failed to read image: {self.SKIN_IMAGE_PATH}")
        if not (
            base_skin_image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT
            and base_skin_image.shape[1] == Effect.EFFECT_IMAGE_WIDTH
        ):
            raise ValueError("Skin image size must be 1024x1024")

        self.skin_image = self._convert_image_color(base_skin_image, hue, sat, val, True)

    def _convert_image_color(
        self, image: np.ndarray, hue: float, sat: float, val: float, include_alpha_ch: bool
    ) -> np.ndarray:
        """アルファチャンネル付きのHSV=(240,255,255)の画像の色を、指定したHSV数値の色に変更する.

        Args:
            image (_type_): H:240 S:255 V:255で塗りつぶしたアルファチャンネルを含むメイク素材、1024x1024
            hue (_type_): HSVのHueの数値(0~255)
            sat (_type_): HSVのSaturationの数値(0~255)
            val (_type_): HSVのValueの数値(0~255)
            include_alpha_ch (_type_): returnする画像にアルファチャンネルを含むか否か
        Return:
            np.ndarray: 任意の色、設定に変更したメイクのnumpy配列
        """
        image_wo_alpha, mask = self._convert_bgra_to_bgr(image, True)
        image_hsv = cv2.cvtColor(image_wo_alpha, cv2.COLOR_BGR2HSV)

        if not (0.0 <= hue <= 255):
            raise ValueError("Defferent range of hue values")
        if not (0.0 <= sat <= 255):
            raise ValueError("Defferent range of sat values")
        if not (0.0 <= val <= 255):
            raise ValueError("Defferent range of val values")

        B255_HUE = 120
        B255_SAT = 255
        NO_CHANGE_VAL = 0
        # OpenCV内でH:120 S:255であり、V:0でないメイクの色が変更可能

        image_hsv[:, :, 0] = np.where(image_hsv[:, :, 0] == B255_HUE, hue / 2, image_hsv[:, :, 0])
        image_hsv[:, :, 1] = np.where(image_hsv[:, :, 1] == B255_SAT, sat, image_hsv[:, :, 1])
        image_hsv[:, :, 2] = np.where(
            image_hsv[:, :, 2] != NO_CHANGE_VAL, (val * (image_hsv[:, :, 2] / 255)), image_hsv[:, :, 2]
        )
        # ↑グラデーションの比率を保ったまま、明度を変更する

        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

        if include_alpha_ch:
            b_ch, g_ch, r_ch = cv2.split(image_bgr[:, :, :3])
            image_bgr_w_alpha = cv2.merge((b_ch, g_ch, r_ch, mask))
            return image_bgr_w_alpha
        else:
            return image_bgr

    @classmethod
    def get_choice_images_paths(cls):
        """Get the paths to the images for the choices."""
        icon_file = cls.ICON_PATH.replace(cls.CHOICE_IMAGES_DIR_PATH, "").replace("/", "")
        return [
            os.path.join(cls.CHOICE_IMAGES_DIR_PATH, file)
            for file in os.listdir(cls.CHOICE_IMAGES_DIR_PATH)
            if file.endswith(".png") and not file == icon_file
        ]

    def _convert_bgra_to_bgr(self, image: np.ndarray, return_mask: bool) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image
            return_mask (_type_): アルファチャンネルの配列をreutrnするかどうか
        Returns:
            _type_: BGR imageもしくは BGRとA
        """
        mask = image[:, :, 3]
        if return_mask:
            return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8), mask
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)
