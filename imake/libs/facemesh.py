# TODO: あまり美しくないラッパーなので、改善したい
# https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/face_mesh.py

from typing import Final

import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh: Final = mp.solutions.face_mesh


class FaceMesh:
    def __init__(
        self,
        max_num_faces: int = 1,
        refine_landmarks: bool = False,  # https://google.github.io/mediapipe/solutions/face_mesh#attention-mesh-model
        static_image_mode: bool = False,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            refine_landmarks=refine_landmarks,
            static_image_mode=static_image_mode,
        )
        self.face_mesh_results = None

    def get_landmarks(self, image: np.ndarray) -> np.ndarray | None:
        """Get landmarks.

        Args:
            image (_type_): image(BGR)

        Returns:
            _type_: landmarks
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.face_mesh_results = self.face_mesh.process(image)

        if not self.face_mesh_results.multi_face_landmarks:  # type: ignore
            return None

        landmarks = []
        for landmark in self.face_mesh_results.multi_face_landmarks[0].landmark:  # type: ignore
            landmarks.append([landmark.x * image.shape[1], landmark.y * image.shape[0], landmark.z])
        return np.array(landmarks)

    def close(self) -> None:
        """Close."""
        self.face_mesh.close()
