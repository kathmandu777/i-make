import sys

import cv2
import numpy as np
from PIL import Image

from .effect import EffectRenderer2D


class Makeup(EffectRenderer2D):
    def __init__(self, makeup_image_paths: list[str], hsv_value_list: list[float], use_filter_points: bool, **kwargs):
        """Initialize Makeup.

        Args:
            makeup_image_paths (list[str]): makeup image paths. リストの先頭から順にメイクを重ねていく
            use_filter_points (bool): use filter landmarks
            **kwargs: keyword arguments for EffectRenderer2D
        """

        effect_image = np.zeros((self.EFFECT_IMAGE_HEIGHT, self.EFFECT_IMAGE_WIDTH, 4), dtype=np.uint8)
        if len(makeup_image_paths) == len(hsv_value_list):
            for image_path, hsv_value in zip(makeup_image_paths, hsv_value_list):
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                if image is None:
                    raise ValueError(f"Failed to read image: {image_path}")
                if not (image.shape[0] == self.EFFECT_IMAGE_HEIGHT and image.shape[1] == self.EFFECT_IMAGE_WIDTH):
                    raise ValueError("Effect image size must be 1024x1024")
                effect_image = self.overlay_alpha_image(effect_image, image, hsv_value)
            super().__init__(effect_image, use_filter_points=use_filter_points, **kwargs)
        else:
            print("The number of image paths and the number of hsv arrays do not match")
            sys.exit()

    def overlay_alpha_image(self, back, front, hsv_value: float):
        """Overlay alpha image on the background image.

        Args:
            back (_type_): background image (RGBA)
            front (_type_): front image (RGBA). The size must be the same as the background image.

        Returns:
            _type_: overlayed image
        """
        convert_color_image = self.convert_color_bgra(back, hsv_value[0], hsv_value[1], hsv_value[2], True)
        back_pil = Image.fromarray(convert_color_image)
        front_pil = Image.fromarray(front)
        image = Image.alpha_composite(back_pil, front_pil)
        print("overlay_alpha_image")
        return np.array(image).astype(np.uint8)

    def convert_bgra_to_bgr(self, image: np.ndarray, return_mask: bool) -> np.ndarray:
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image
            return_mask (_type_):アルファチャンネルの配列をreutrnするかどうか
        Returns:
            _type_: BGR imageもしくは BGRとA
        """
        mask = image[:, :, 3]
        if return_mask:
            return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8), mask
        else:
            return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)

    def convert_color_bgra(
        self, image: np.ndarray, hue: float, saturation: float, value: float, include_alpha_ch: bool
    ) -> np.ndarray:
        """指定したHSVにメイクを変更する.

        Args:
            image(_type_): B255で塗りつぶした透過メイク素材、1024x1024
            hue(_type_):HSVのHueの数値
            saturation(_type_):HSVのSaturationの数値
            value(_type_):HSVのVvalueの数値
            include_alpha_ch(_type_):returnする画像にアルファチャンネルを含むか否か
        Return:
            np.ndarray:任意の色、設定に変更したメイクのnumpy配列
        """
        print("color")
        image_wo_alpha, mask = self.convert_bgra_to_bgr(image, True)
        image_hsv = cv2.cvtColor(image_wo_alpha, cv2.COLOR_BGR2HSV)

        image_hsv[:, :, 0] = np.where(image_hsv[:, :, 0] == 120, hue / 2, image_hsv[:, :, 0])
        image_hsv[:, :, 1] = np.where(image_hsv[:, :, 1] == 255, saturation, image_hsv[:, :, 1])
        image_hsv[:, :, 2] = np.where(
            image_hsv[:, :, 2] != 0, (value * (image_hsv[:, :, 2] / 255)), image_hsv[:, :, 2]
        )
        # ↑グラデーションの比率を保ったまま、明度を変更する

        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

        if include_alpha_ch:
            b_ch, g_ch, r_ch = cv2.split(image_bgr[:, :, :3])
            image_bgr_w_alpha = cv2.merge((b_ch, g_ch, r_ch, mask))
            return image_bgr_w_alpha
        else:
            return image_bgr
