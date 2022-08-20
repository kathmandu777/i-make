from pickletools import uint8
from tempfile import NamedTemporaryFile
from typing import Tuple
import cv2
import numpy as np


class EffectRenderer2D:
    def __init__(
        self,
        effect_image_path,
        src_points_path="./gen2-facemesh/res/source_landmarks.npy",
        filter_points_path="./gen2-facemesh/res/filter_points.npy",
    ):

        self.effect_image = cv2.imread(effect_image_path, cv2.IMREAD_UNCHANGED)
        self.need_face_points = np.load(src_points_path)
        #顔全体の座標

        self.filter_points = np.load(filter_points_path)
        self.need_face_points = self.need_face_points[self.filter_points]
        #必要な座標

        self.subdiv = cv2.Subdiv2D((0, 0, self.effect_image.shape[1], self.effect_image.shape[0]))
        self.subdiv.insert(self.need_face_points.tolist())
        #ドロネー図オブジェクトを作成し、そこに結びたい座標をインサートしている

        self.triangles = np.array(
            [
                (self.need_face_points == value).all(axis=1).nonzero()
                for element in self.subdiv.getTriangleList()
                for value in element.reshape((3, 2))
            ]
        )
        self.triangles = self.triangles.reshape(len(self.triangles) // 3, 3)
    
    """
    initialization
    Args:
        effect_image_path:貼り付けたい画像のパス,1024x1024が好ましい
        src_points_path:顔全体のランドマークのnumpy配列データ
        filter_points_path:顔の必要な部分のランドマークのnumpy配列データ
    """

    def render_effect(self, target_image:uint8, target_landmarks:float)->uint8:
        """
        進行用の関数。これに値を入れて返り値をcv2.imshowすると画面上に表示できる
        Args:
            target_image(uint8):カメラから入力された映像
            target_landmarks(float64):カメラを素に作成したランドマーク
        Returns:
            uint8:cv2.imshowできるデータ
        """
        need_face_landmarks = target_landmarks[self.filter_points]
        effect = self.create_effect(target_image, need_face_landmarks)
        return self.overlay_image(target_image, effect)

    def create_effect(self, target_image:uint8, face_points:float)->uint8:
        """Creates effect image that can be rendered on the target image.

        :param target_image: target image
        :param dst_points: landmarks on the target image, should be of the same size and order as self.filter_points
        :return: effect image
        -----------------------------------------
        ↑公式見解
        -----------------------------------------
        元データをこの関数からcrop_triangle_bbへ移しそこから渡された三角データを
        アフィン変換する関数。
        Args:
            target_image(uint8):カメラから入力された映像
            face_points(float64):必要な顔の座標
        Returns:
            uint8:ゼロ配列を返す、後のoverlay_imageで使用する
        """

        # create empty overlay
        overlay = np.zeros((target_image.shape[0], target_image.shape[1], 4), np.uint8)

        for idx_tri in self.triangles:
            src_tri = self.need_face_points[idx_tri]
            dst_tri_full = face_points[idx_tri]
            dst_tri = dst_tri_full[:, :2].astype(np.int32)

            src_tri_crop, src_crop = self.crop_triangle_bb(self.effect_image, src_tri)
            dst_tri_crop, overlay_crop = self.crop_triangle_bb(overlay, dst_tri)

            warp_mat = cv2.getAffineTransform(np.float32(src_tri_crop), np.float32(dst_tri_crop))
            warp = cv2.warpAffine(
                src_crop,
                warp_mat,
                (overlay_crop.shape[1], overlay_crop.shape[0]),
                None,
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT_101,
            )

            mask = np.zeros((overlay_crop.shape[0], overlay_crop.shape[1], 4), dtype=np.uint8)
            cv2.fillConvexPoly(mask, np.int32(dst_tri_crop), (1.0, 1.0, 1.0, 1.0), 16, 0)
            mask[np.where(overlay_crop > 0)] = 0

            cropped_triangle = warp * mask
            overlay_crop += cropped_triangle

        return overlay

    def overlay_image(self, background_image, foreground_image, blur=0):
        """Take the two images, and produce an image where foreground image
        overlays the background image.

        :param background_image: background BRG or BGRA image with 0-255 values, transparency will be ignored in the result
        :param foreground_image: foreground BGRA image with 0-255 values
        :return: BGR image with foreground image overlaying the background image
        -----------------------------------------
        ↑公式見解
        -----------------------------------------
        元のデータを三角形状にパーツ化しマスクを作成する処理
        Args:
            target_image(uint8):カメラから入力された映像
            face_points(float64):必要な顔の座標
        Returns:
            uint8:ゼロ配列を返す、後のoverlay_imageで使用する
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

    def crop_triangle_bb(self, image, triangle)->Tuple[int,int]:
        """Create a trinagle bounding box and return cropped image.

        :param image: Target image
        :param triangle: Triangle coordinates (3x2 array)
        :return: Tupple (Triangle crop coordinates relative to the cropped image, cropped image)
        -----------------------------------------
        ↑公式見解
        -----------------------------------------
        元のデータを三角形状にパーツ化する処理
        Args:
            image(uint8):カメラから入力された映像
            triangle(uint32):必要な顔の座標
        Returns:
            triangle_crop(uint64):三角の座標データ
            crop(uint8):三角の映像データ
        """
        x, y, w, h = cv2.boundingRect(triangle)
        crop = image[y : y + h, x : x + w]
        triangle_crop = triangle - np.array([x, y])
        return triangle_crop, crop
