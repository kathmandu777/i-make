import argparse

import cv2
import mediapipe as mp
import numpy as np

from .libs.makeup import Makeup

parser = argparse.ArgumentParser()
parser.add_argument(
    "-detect_conf", "--detection_confidence", help="set the detection confidence threshold", default=0.5, type=float
)
parser.add_argument(
    "-track_conf", "--tracking_confidence", help="set the tracking confidence threshold", default=0.5, type=float
)

args = parser.parse_args()
SKIN_IMAGE = "i-make/static/facepaints/custom/skin/skin0.png"
EYE_BAGS_IMAGE = "i-make/static/facepaints/custom/eye-bags/eye-bags0.png"
EYE_SHADOW_IMAGE = "i-make/static/facepaints/custom/eye-shadow/eye-shadow0-0.png"
GLITTER_IMAGE = "i-make/static/facepaints/custom/glitter/u-glitterL.png"
EYE_LINE_IMAGE = "i-make/static/facepaints/custom/eyeliner/eyeliner0-0.png"
EYE_LASH_IMAGE = "i-make/static/facepaints/custom/eyelashes/eyelashes0-0.png"
HALLOWEEN = "i-make/static/facepaints/event/Halloween0.png"
TEST = "/home/gorugo/i-make/i-make/static/facepaints/B255.png"

mp_face_mesh = mp.solutions.face_mesh
makeup = Makeup(
    [TEST],
    [[0, 255, 255]],
    use_filter_points=True,
)
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
            effected_image_w_alpha = makeup.render_effect(
                target_image, np.array(landmarks), do_overlay=False, mirror=True
            )
            effected_image = makeup.convert_bgra_to_bgr(effected_image_w_alpha, False)
        else:
            effected_image = image.copy()

        cv2.imshow("RESULT", effected_image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
