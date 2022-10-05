from typing import Final, Tuple

import cv2
import numpy as np


class Effect:
    EFFECT_IMAGE_WIDTH: Final = 1024
    EFFECT_IMAGE_HEIGHT: Final = 1024
    SRC_POINTS_PATH: Final = "imake/res/source_landmarks.npy"
    FILTER_POINTS_PATH: Final = "imake/res/filter_points.npy"

    def __init__(
        self,
        effect_image: np.ndarray | None = None,
        use_filter_points: bool = True,
    ):
        """Initialize Effect.

        Args:
            effect_image (np.ndarray): effect image (1024 x 1024)
            use_filter_points (bool, optional): use filter landmarks. Defaults to True. (If False, use all landmarks)
        """
        if effect_image is not None:
            self.set_effect_image(effect_image)

        self.src_points = np.load(self.SRC_POINTS_PATH)  # facemeshが返却する468(467)個のランドマークの座標
        self.filter_points = np.load(self.FILTER_POINTS_PATH)  # src_pointsの中から選択するランドマークのindex

        self.use_filter_points = use_filter_points
        if use_filter_points:
            self.src_points = self.src_points[self.filter_points]

        self.subdiv = cv2.Subdiv2D(
            (0, 0, self.EFFECT_IMAGE_WIDTH, self.EFFECT_IMAGE_HEIGHT)
        )  # cv2.Subdiv2D((left, top, right, bottom))
        self.subdiv.insert(self.src_points.tolist())  # 対象の点を追加

        self.triangles_1D = np.array(
            [
                (self.src_points == value).all(axis=1).nonzero()
                for element in self.subdiv.getTriangleList()  # ドロネー三角形を取得 element=[1個目のx座標 1個目のy座標 2個目のx座標 2個目のy座標 3個目のx座標 3個目のy座標]
                for value in element.reshape((3, 2))
            ]
        )
        self.triangles = self.triangles_1D.reshape(len(self.triangles_1D) // 3, 3)

    def set_effect_image(self, effect_image: np.ndarray) -> None:
        """Set effect image.

        Args:
            effect_image (np.ndarray): effect image (1024 x 1024)
        """
        if not (
            effect_image.shape[0] == self.EFFECT_IMAGE_HEIGHT and effect_image.shape[1] == self.EFFECT_IMAGE_WIDTH
        ):
            raise ValueError("Effect image size must be 1024x1024")
        self.effect_image = effect_image

    def _create_effect(self, target_image: np.ndarray, target_landmarks: np.ndarray) -> np.ndarray:
        """Creates effect image that can be rendered into an image the size of
        the target image.

        Args:
            target_image (np.ndarray): target image
            target_landmarks (np.ndarray): landmarks on the target image. Must be the same size as the source landmarks.

        Returns:
            np.ndarray: effect image (BGRA)
        """
        if self.effect_image is None:
            raise ValueError("Effect image is not set")

        if self.use_filter_points:
            target_landmarks = target_landmarks[self.filter_points]

        # create empty overlay
        overlay = np.zeros((target_image.shape[0], target_image.shape[1], 4), np.uint8)

        for idx_tri in self.triangles:
            src_tri = self.src_points[idx_tri]
            dst_tri_full = target_landmarks[idx_tri]
            dst_tri = dst_tri_full[:, :2].astype(np.int32)

            src_tri_crop, src_crop = self._crop_triangle_bb(self.effect_image, src_tri)
            dst_tri_crop, overlay_crop = self._crop_triangle_bb(overlay, dst_tri)

            warp_mat = cv2.getAffineTransform(np.float32(src_tri_crop), np.float32(dst_tri_crop))  # アフィン変換の変換行列を取得
            warp = cv2.warpAffine(
                src_crop,
                warp_mat,
                (overlay_crop.shape[1], overlay_crop.shape[0]),
                None,
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT_101,
            )

            mask = np.zeros((overlay_crop.shape[0], overlay_crop.shape[1], 4), dtype=np.uint8)  # shapeが一つでも0になるとエラーになる
            if mask.shape[0] != 0 and mask.shape[1] != 0:
                cv2.fillConvexPoly(
                    mask, np.int32(dst_tri_crop), (1.0, 1.0, 1.0, 1.0), 16, 0
                )  # 多角形を描画 fillConvexPoly(元の画像, 複数の座標, color, ...)
                mask[np.where(overlay_crop > 0)] = 0

                cropped_triangle = warp * mask
                overlay_crop += cropped_triangle

        return overlay

    def _crop_triangle_bb(self, image: np.ndarray, triangle: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create a triangle bounding box and return cropped image.

        Args:
            image (np.ndarray): target image
            triangle (np.ndarray): Triangle coordinates (3x2 array)

        Returns:
            _type_: Tupple (Triangle crop coordinates relative to the cropped image, cropped image)
        """
        x, y, w, h = cv2.boundingRect(triangle)  # 外接矩形(回転なし)
        crop = image[y : y + h, x : x + w]
        triangle_crop = triangle - np.array([x, y])
        return triangle_crop, crop
