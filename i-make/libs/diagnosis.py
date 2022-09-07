from typing import Tuple

import cv2
import numpy as np


class EyeDiagnosis:
    LEFT_EYE_LEFTMOST_IDX = 33
    LEFT_EYE_RIGHTMOST_IDX = 133
    RIGHT_EYE_LEFTMOST_IDX = 362
    RIGHT_EYE_RIGHTMOST_IDX = 263

    def __init__(self, threshold: float = 0.2):
        self.PROPER_RATIO_THRESHOLD = threshold

    def render_eye_edge(
        self, landmarks: np.ndarray, image: np.ndarray, radius: int = 1, color: Tuple[int, int, int] = (0, 0, 255)
    ) -> np.ndarray:
        """左右の目の端に点を描画する.

        Args:
            landmarks (_type_): 顔のランドマーク
            image (_type_): 描画する画像
            radius (int, optional): 半径. Defaults to 1.
            color (tuple, optional): 点の色. Defaults to (0, 0, 255).

        Returns:
            _type_: 描画した画像
        """
        for idx in (
            self.LEFT_EYE_LEFTMOST_IDX,
            self.LEFT_EYE_RIGHTMOST_IDX,
            self.RIGHT_EYE_LEFTMOST_IDX,
            self.RIGHT_EYE_RIGHTMOST_IDX,
        ):
            cv2.circle(image, (int(landmarks[idx][0]), int(landmarks[idx][1])), radius, color, -1)
        return image

    def calculate_eye_size(self, landmarks: np.ndarray, leftmost_idx: int, rightmost_idx: int) -> float:
        """目のX軸の長さを計算する.

        Args:
            landmarks (_type_): 顔のランドマーク
            leftmost_idx (_type_): 目の左端のランドマークのインデックス
            rightmost_idx (_type_): 目の右端のランドマークのインデックス

        Returns:
            _type_: 目のX軸の長さ
        """
        leftmost: Tuple[float, float, float] = landmarks[leftmost_idx]
        rightmost: Tuple[float, float, float] = landmarks[rightmost_idx]
        return rightmost[0] - leftmost[0]

    def calculate_left_eye_size(self, landmarks: np.ndarray) -> float:
        """左目のX軸の長さを計算する.

        Args:
            landmarks (_type_): 顔のランドマーク

        Returns:
            float: 左目のX軸の長さ
        """
        return self.calculate_eye_size(landmarks, self.LEFT_EYE_LEFTMOST_IDX, self.LEFT_EYE_RIGHTMOST_IDX)

    def calculate_right_eye_size(self, landmarks: np.ndarray) -> float:
        """右目のX軸の長さを計算する.

        Args:
            landmarks (_type_): 顔のランドマーク

        Returns:
            float: 右目のX軸の長さ
        """
        return self.calculate_eye_size(landmarks, self.RIGHT_EYE_LEFTMOST_IDX, self.RIGHT_EYE_RIGHTMOST_IDX)

    def calculate_eye_ratio(self, landmarks: np.ndarray) -> float:
        """目の比率を計算する.

        Args:
            landmarks (_type_): 顔のランドマーク

        Returns:
            float: 目の比率
        """
        left_eye_size = self.calculate_left_eye_size(landmarks)
        right_eye_size = self.calculate_right_eye_size(landmarks)
        return left_eye_size / right_eye_size

    def calculate_distance_between_eye(self, landmarks: np.ndarray) -> float:
        """目の間のX軸の距離を計算する.

        Args:
            landmarks (_type_): 顔のランドマーク

        Returns:
            float: 目の間のX軸の距離
        """
        left_eye_rightmost: Tuple[float, float, float] = landmarks[self.LEFT_EYE_RIGHTMOST_IDX]
        right_eye_leftmost: Tuple[float, float, float] = landmarks[self.RIGHT_EYE_LEFTMOST_IDX]
        return right_eye_leftmost[0] - left_eye_rightmost[0]

    def is_longer_distance_between_eye_than_eye_size(self, landmarks: np.ndarray) -> bool | None:
        """目のサイズより目の間の距離が長いかどうかを判定する.

        Args:
            landmarks (_type_): 顔のランドマーク

        Returns:
            bool | None: 目のサイズより目の間の距離が長いかどうか (Noneの場合は正面を向いていない)
        """
        left_eye_size = self.calculate_left_eye_size(landmarks)
        right_eye_size = self.calculate_right_eye_size(landmarks)
        eye_ratio = self.calculate_eye_ratio(landmarks)
        if eye_ratio < 1.0 - self.PROPER_RATIO_THRESHOLD or eye_ratio > 1.0 + self.PROPER_RATIO_THRESHOLD:
            return None
        distance_between_eye = self.calculate_distance_between_eye(landmarks)
        return distance_between_eye > (left_eye_size + right_eye_size) / 2
