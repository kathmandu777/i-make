#!/usr/bin/env python3

import argparse

import cv2
import mediapipe as mp
import numpy as np
from utils.effect import EffectRenderer2D

"""
MediaPipe Facial Landmark detector with PNG EffectRenderer using web camera.
Run as:
python3 -m pip install -r requirements_web_camera.txt
python3 main_web_camera.py -detect_conf [DETECT_CONF] -track_conf [TRACK_CONF]
"""


parser = argparse.ArgumentParser()
parser.add_argument(
    "-detect_conf", "--detection_confidence", help="set the detection confidence threshold", default=0.5, type=float
)
parser.add_argument(
    "-track_conf", "--tracking_confidence", help="set the tracking confidence threshold", default=0.5, type=float
)

args = parser.parse_args()
OVERLAY_IMAGE = "mask/facepaint.png"

mp_face_mesh = mp.solutions.face_mesh
renderer_1 = EffectRenderer2D(OVERLAY_IMAGE, use_filter_points=True)
renderer_2 = EffectRenderer2D(OVERLAY_IMAGE, use_filter_points=False)

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
            effected_image_1 = renderer_1.render_effect(target_image, np.array(landmarks))
            effected_image_2 = renderer_2.render_effect(target_image, np.array(landmarks))
        else:
            effected_image_1 = effected_image_2 = image.copy()

        cv2.imshow(
            "Demo", np.hstack([cv2.flip(image, 1), cv2.flip(effected_image_1, 1), cv2.flip(effected_image_2, 1)])
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
