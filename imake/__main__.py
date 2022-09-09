import argparse

import cv2
import mediapipe as mp
import numpy as np

from .libs.effect import EffectRenderer2D

parser = argparse.ArgumentParser()
parser.add_argument(
    "-detect_conf", "--detection_confidence", help="set the detection confidence threshold", default=0.5, type=float
)
parser.add_argument(
    "-track_conf", "--tracking_confidence", help="set the tracking confidence threshold", default=0.5, type=float
)

args = parser.parse_args()
OVERLAY_IMAGE = "i-make/static/facepaints/facepaint.png"

mp_face_mesh = mp.solutions.face_mesh
renderer_1 = EffectRenderer2D(OVERLAY_IMAGE, use_filter_points=True)
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=args.detection_confidence,
    min_tracking_confidence=args.tracking_confidence,
) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            landmarks = []
            for landmark in results.multi_face_landmarks[0].landmark:
                landmarks.append([landmark.x * image.shape[1], landmark.y * image.shape[0], landmark.z])
            target_image = image.copy()
            effected_image = renderer_1.render_effect(target_image, np.array(landmarks), False)
        else:
            effected_image = image.copy()

        cv2.imshow("RESULT", effected_image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
