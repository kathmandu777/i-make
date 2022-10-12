# https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/face_mesh.py

from typing import Final

import cv2
import mediapipe as mp
import numpy as np

mp_face_detection: Final = mp.solutions.face_detection


class FaceDetection:
    def __init__(
        self,
        model_selection: int = 0,  # 0=within 2m, 1=within 5m
        min_detection_confidence: float = 0.5,
    ):
        self.face_detection = mp_face_detection.FaceDetection(
            model_selection=model_selection,
            min_detection_confidence=min_detection_confidence,
        )

    def get_bounding_box(self, image: np.ndarray) -> dict[str, float]:
        """Get landmarks.

        Args:
            image (np.ndarray): image(BGR)

        Returns:
            _type_: landmarks
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image)

        if not results.detections:  # type: ignore
            raise Exception("No face detected.")

        return results.detections[0].location_data.relative_bounding_box  # type: ignore

    def close(self) -> None:
        """Close."""
        self.face_detection.close()
