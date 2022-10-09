import os
from dataclasses import asdict
from typing import Any, Final

import cv2
import numpy as np
from PIL import Image

from ..dataclasses import HSV, FacePaint
from ..libs.effect import Effect


class BaseMode:
    """Base class for all modes."""

    ICON_PATH: str
    MENU_IMAGE_PATH: str

    @classmethod
    def icon_path_for_frontend(cls) -> str:
        """Return icon path for frontend.

        Returns:
            str: icon path
        """
        return "../" + cls.ICON_PATH.replace("imake/static/", "")

    @classmethod
    def menu_image_path_for_frontend(cls) -> str:
        """Return menu image path for frontend.

        Returns:
            str: menu image path
        """
        return "../" + cls.MENU_IMAGE_PATH.replace("imake/static/", "")


class BaseModeEffect(BaseMode, Effect):
    """Base class for all modes that use Effect."""

    # Path to the directory containing the images for the choices and thumbnails. Must be overridden.
    MAKEUP_IMAGES_DIR_PATH: str
    THUMBNAILS_DIR_PATH: str

    SKIN_IMAGE_PATH: Final = "imake/static/modes/custom/skin/skin.png"

    B255_HUE: Final = 120
    B255_SAT: Final = 255
    NO_CHANGE_VAL: Final = 0

    BASE_IMAGE_SUFFIX: Final = "-base.png"  # ２枚重ねによって作られるメイク画像の色変更をしない方の画像名のsuffix

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:

        super().__init__(*args, **kwargs)

    @classmethod
    def get_class_vars(cls) -> dict[str, Any]:
        """Get the class variables.

        Returns:
            dict[str, Any]: class variables.
        """
        return {key: value for key, value in vars(cls).items() if not key.startswith("__")}

    def set_effect_image_by_facepaints(self, facepaints: list[FacePaint]) -> None:
        """Set effect image from path.

        Args:
            facepaints (_type_): list of FacePaint
        """
        self.set_effect_image(self._overlay_effect_images(facepaints))

    def _overlay_effect_images(self, facepaints: list[FacePaint]) -> np.ndarray:
        """Overlay effect images on skin image.

        Args:
            facepaints (_type_): list of FacePaint
        Returns:
            np.ndarray: effect image for EffectCreator
        """
        if self.skin_image is None:
            raise ValueError("skin_image is None")

        effect_image = self.skin_image
        for facepaint in facepaints:
            image = cv2.imread(facepaint.image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise Exception(f"Failed to read image: {facepaint.image_path}")
            if not (image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT and image.shape[1] == Effect.EFFECT_IMAGE_WIDTH):
                raise ValueError("Effect image size must be 1024x1024")

            base_image_path = facepaint.image_path.replace(
                ".png", self.BASE_IMAGE_SUFFIX
            )  # ２枚重ねによって作られるメイク画像の色変更をしない方の画像名
            if os.path.exists(base_image_path):
                base_image = cv2.imread(base_image_path, cv2.IMREAD_UNCHANGED)
                if base_image is None:
                    raise Exception(f"Failed to read image: {base_image_path}")
                if not (
                    base_image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT
                    and base_image.shape[1] == Effect.EFFECT_IMAGE_WIDTH
                ):
                    raise ValueError("Base image size must be 1024x1024")
                image = self._overlay_alpha_image(effect_image, base_image)

            image = self._convert_image_color(image, facepaint.hsv, True) if facepaint.hsv is not None else image
            effect_image = self._overlay_alpha_image(effect_image, image)
        return effect_image

    def _overlay_alpha_image(self, back: np.ndarray, front: np.ndarray) -> np.ndarray:
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

    def set_skin_color(self, hsv: HSV) -> None:
        """指定したHSVにスキンカラーをセットする.

        Args:
            hsv (HSV): HSV
        """
        base_skin_image = cv2.imread(self.SKIN_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
        if base_skin_image is None:
            raise Exception(f"Failed to read image: {self.SKIN_IMAGE_PATH}")
        if not (
            base_skin_image.shape[0] == Effect.EFFECT_IMAGE_HEIGHT
            and base_skin_image.shape[1] == Effect.EFFECT_IMAGE_WIDTH
        ):
            raise ValueError("Skin image size must be 1024x1024")

        self.skin_image = self._convert_image_color(base_skin_image, hsv, True)

    def _convert_image_color(self, image: np.ndarray, hsv: HSV, include_alpha_ch: bool) -> np.ndarray:
        """アルファチャンネル付きのRGB=(0,0,255)の画像の色を、指定したHSV数値の色に変更する.

        Args:
            image (np.ndarray): RGB=(0,0,255)で塗りつぶしたアルファチャンネルを含むメイク素材、1024x1024
            hsv (HSV): HSV
            include_alpha_ch (bool): returnする画像にアルファチャンネルを含むか否か
        Return:
            np.ndarray: 任意の色、設定に変更したメイクのnumpy配列
        """
        # opencvでのHSVの範囲は0-180,0-255,0-255
        hue = hsv.h / 2
        sat = hsv.s / 100 * 255
        val = hsv.v / 100 * 255
        image_wo_alpha, mask = self._convert_bgra_to_bgr(image)
        image_hsv = cv2.cvtColor(image_wo_alpha, cv2.COLOR_BGR2HSV)

        image_hsv[:, :, 0] = np.where(image_hsv[:, :, 0] == self.B255_HUE, hue, image_hsv[:, :, 0])
        image_hsv[:, :, 1] = np.where(image_hsv[:, :, 1] == self.B255_SAT, sat, image_hsv[:, :, 1])
        image_hsv[:, :, 2] = np.where(
            image_hsv[:, :, 2] != self.NO_CHANGE_VAL, (val * (image_hsv[:, :, 2] / 255)), image_hsv[:, :, 2]
        )
        # ↑グラデーションの比率を保ったまま、明度を変更する

        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

        if include_alpha_ch:
            b_ch, g_ch, r_ch = cv2.split(image_bgr[:, :, :3])
            image_bgr_w_alpha = cv2.merge((b_ch, g_ch, r_ch, mask))
            return image_bgr_w_alpha
        else:
            return image_bgr

    def _convert_bgra_to_bgr(self, image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Convert RGBA image to RGB image.

        Args:
            image (np.ndarray): RGBA image
        Returns:
            _type_: BGRとA
        """
        mask = image[:, :, 3]
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8), mask

    @classmethod
    def get_choice_facepaints(cls) -> list[dict]:
        """選択肢のメイクを取得する.

        Returns:
            list[FacePaint]: メイクのリスト
        """
        icon_file = cls.ICON_PATH.replace(cls.MAKEUP_IMAGES_DIR_PATH, "").replace("/", "")
        menu_image_file = cls.MENU_IMAGE_PATH.replace(cls.MAKEUP_IMAGES_DIR_PATH, "").replace("/", "")
        facepaints = [
            FacePaint(
                filename=file,
                image_dir_path=cls.MAKEUP_IMAGES_DIR_PATH,
                thumbnail_dir_path=cls.THUMBNAILS_DIR_PATH,
            )
            for file in os.listdir(cls.MAKEUP_IMAGES_DIR_PATH)
            if (file.endswith(".png") or file.endswith(".PNG"))
            and file != menu_image_file
            and file != icon_file
            and not (cls.BASE_IMAGE_SUFFIX in file)
        ]
        return [
            {
                **asdict(facepaint),
                # FIXME: facepaintのpropertyもasdictに含めたい
                "thumbnail_path_for_frontend": facepaint.thumbnail_path_for_frontend,
                "image_path": facepaint.image_path,  # FIXME: ditto
            }
            for facepaint in facepaints
        ]
