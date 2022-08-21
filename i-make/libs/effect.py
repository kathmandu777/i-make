from typing import Tuple

import cv2
import numpy as np


class EffectRenderer2D:
    def __init__(
        self,
        effect_image_path: str,
        src_points_path: str = "i-make/res/source_landmarks.npy",
        filter_points_path: str = "i-make/res/filter_points.npy",
        use_filter_points: bool = True,
    ):
        """Initialize EffectRenderer2D.

        Args:
            effect_image_path (str): path to the effect image (1024 x 1024)
            src_points_path (str, optional): path to the source landmarks. Defaults to "i-make/res/source_landmarks.npy".
            filter_points_path (str, optional): path to the filter landmarks. Defaults to "i-make/res/filter_points.npy".
            use_filter_points (bool, optional): use filter landmarks. Defaults to True.
        """

        self.effect_image = cv2.imread(effect_image_path, cv2.IMREAD_UNCHANGED)
        height, width, _ = self.effect_image.shape

        self.src_points = np.load(src_points_path)  # facemeshが返却する468(467)個のランドマークの座標
        self.filter_points = np.load(filter_points_path)  # src_pointsの中から選択するランドマークのindex

        self.use_filter_points = use_filter_points
        if use_filter_points:
            self.src_points = self.src_points[self.filter_points]

        self.subdiv = cv2.Subdiv2D((0, 0, width, height))  # cv2.Subdiv2D((left, top, right, bottom))
        self.subdiv.insert(self.src_points.tolist())  # 対象の点を追加

        self.triangles_1D = np.array(
            [
                (self.src_points == value).all(axis=1).nonzero()
                for element in self.subdiv.getTriangleList()  # ドロネー三角形を取得 element=[1個目のx座標 1個目のy座標 2個目のx座標 2個目のy座標 3個目のx座標 3個目のy座標]
                for value in element.reshape((3, 2))
            ]
        )
        self.triangles = self.triangles_1D.reshape(len(self.triangles_1D) // 3, 3)

    def render_effect(self, target_image: np.ndarray, target_landmarks: np.ndarray) -> np.ndarray:
        """Render effect on the target image.

        Args:
            target_image (_type_): 描画する画像(カメラ画像)
            target_landmarks (_type_): target_image上でのランドマークの座標

        Returns:
            np.array: 描画された画像
        """
        if self.use_filter_points:
            target_landmarks = target_landmarks[self.filter_points]
        effect = self.create_effect(target_image, target_landmarks)
        return self.overlay_image(target_image, effect)

    def create_effect(self, target_image: np.ndarray, dst_points: np.ndarray) -> np.ndarray:
        """Creates effect image that can be rendered on the target image.

        Args:
            target_image (_type_): target image
            dst_points (_type_): landmarks on the target image, should be of the same size and order as self.filter_points

        Returns:
            _type_: effect image
        """

        # create empty overlay
        overlay = np.zeros((target_image.shape[0], target_image.shape[1], 4), np.uint8)

        for idx_tri in self.triangles:
            src_tri = self.src_points[idx_tri]
            dst_tri_full = dst_points[idx_tri]
            dst_tri = dst_tri_full[:, :2].astype(np.int32)

            src_tri_crop, src_crop = self.crop_triangle_bb(self.effect_image, src_tri)
            dst_tri_crop, overlay_crop = self.crop_triangle_bb(overlay, dst_tri)

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

    def overlay_image(self, background_image: np.ndarray, foreground_image: np.ndarray, blur: float = 0) -> np.ndarray:
        """Take the two images, and produce an image where foreground image
        overlays the background image.

        Args:
            background_image (_type_): background BRG or BGRA image with 0-255 values, transparency will be ignored in the result
            foreground_image (_type_): foreground BGRA image with 0-255 values
            blur (int, optional): blur. Defaults to 0.

        Returns:
            _type_: BGR image with foreground image overlaying the background image
        """

        mask = foreground_image[:, :, 3]

        if blur > 0:
            mask = cv2.medianBlur(mask, blur)

        mask_inv = 255 - mask

        overlayed = foreground_image[:, :, :3] * np.dstack([mask / 255.0] * 3) + background_image[
            :, :, :3
        ] * np.dstack([mask_inv / 255.0] * 3)
        overlayed = overlayed.astype(np.uint8)

        return overlayed

    def crop_triangle_bb(self, image: np.ndarray, triangle: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create a trinagle bounding box and return cropped image.

        Args:
            image (_type_): target image
            triangle (_type_): Triangle coordinates (3x2 array)

        Returns:
            _type_: Tupple (Triangle crop coordinates relative to the cropped image, cropped image)
        """
        x, y, w, h = cv2.boundingRect(triangle)  # 外接矩形(回転なし)
        crop = image[y : y + h, x : x + w]
        triangle_crop = triangle - np.array([x, y])
        return triangle_crop, crop
