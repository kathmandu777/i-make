import argparse
import base64
from dataclasses import asdict
from typing import Final

import cv2
import eel
import numpy as np

from .dataclasses import HSV, FacePaint
from .dataclasses.diagnosis import Choice
from .libs.diagnosis import EyeDiagnosis
from .libs.facemesh import FaceMesh
from .mode import BaseModeEffectType, CustomMode, DiagnosisMode, Mode


class iMake:
    EEL_SLEEP_TIME: Final = 0.00000001

    def __init__(self, camera_id: int = 0):
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)

        self.skin_hsv = HSV(h=14, s=36, v=100)
        self.back_process = None

    def set_mode(self, mode_name: str, *args, **kwargs):
        """Set mode.

        Args:
            mode_name (_type_): mode name
        """
        self.mode: BaseModeEffectType = Mode[mode_name].value(**kwargs)

    def get_mode_choices(self) -> list[dict[str, str]]:
        """Get mode choices."""
        return [
            {
                "name": mode.name,
                "icon_path": mode.value.icon_path_for_frontend(),
                "menu_image_path": mode.value.menu_image_path_for_frontend(),
            }
            for mode in Mode
        ]

    def set_effect_image(self, facepaints: list[dict] | dict) -> None:
        """Set effect image from path.

        Args:
            facepaints (_type_): facepaint
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        if isinstance(facepaints, dict):
            facepaints = [facepaints]

        self.mode.set_skin_color(self.skin_hsv)
        self.mode.set_effect_image_by_facepaints([FacePaint(**facepaint) for facepaint in facepaints])

    def get_choice_facepaints(self) -> list[dict]:
        """Get choice facepaints.

        Returns:
            _type_: choice facepaints
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return self.mode.get_choice_facepaints()

    def set_skin_color(self, hsv: dict):
        """Set skin color.

        Args:
           hue (float, optional): HSVのHueの数値
           sat (float, optional): HSVのSaturationの数値
           val (float, optional): HSVのValueの数値
           include_alpha_ch (bool, optional): setする画像にアルファチャンネルを含むか否か
        """
        self.skin_hsv = HSV(**hsv)

    def get_hsv_palette(self) -> list[dict]:
        """Get color palette.

        Returns:
            _type_: color palette
        """
        palette = [
            HSV(h=14, s=36, v=100),
            HSV(h=27, s=36, v=100),
            HSV(h=41, s=74, v=55),
            HSV(h=40, s=51, v=86),
            HSV(h=15, s=45, v=82),
        ]
        return [asdict(hsv) for hsv in palette]

    def _process(self, mirror: bool = True) -> np.ndarray | None:
        """Process.

        Returns:
            _type_: effect(BGR)
        """
        image = self._get_image()
        if image is None:
            return None

        landmarks = self.face_mesh.get_landmarks(image)
        if landmarks is None:
            return None

        effect_w_alpha = self.mode._create_effect(image, landmarks)
        effect = self._convert_rgba_to_rgb(effect_w_alpha)
        cropped = self._crop_center_x(effect)
        return cv2.flip(cropped, 1) if mirror else cropped

    def start(self):
        """Start."""
        self._kill_back_process()
        self.back_process = eel.spawn(self._start)

    def _start(self):
        while True:
            eel.sleep(self.EEL_SLEEP_TIME)
            effect = self._process()
            if effect is None:
                continue

            _, imencode_image = cv2.imencode(".jpg", effect)
            base64_image = base64.b64encode(imencode_image)
            eel.setVideoSrc("data:image/jpg;base64," + base64_image.decode("ascii"))

    def stop(self):
        self._kill_back_process()
        eel.setVideoSrc("/dist/guide.png")

    def _get_image(self) -> np.ndarray | None:
        """Get image.

        Returns:
            _type_: image
        """
        ret, image = self.cap.read()
        if not ret:
            print("failed to get image")
            return None
        return image

    def _convert_rgba_to_rgb(self, image: np.ndarray) -> np.ndarray:
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image

        Returns:
            _type_: RGB image
        """
        mask = image[:, :, 3]
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)

    def _crop_center_x(self, image: np.ndarray) -> np.ndarray:
        """Crop center x.

        Args:
            image (_type_): image

        Returns:
            _type_: image
        """
        return image[:, image.shape[1] // 4 : image.shape[1] * 3 // 4, :]

    def get_config(self):
        """Get config.

        Returns:
            _type_: config
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return self.mode.get_class_vars()

    def _kill_back_process(self):
        """Kill back process."""
        if self.back_process is not None:
            self.back_process.kill()

    def close(self):
        self.cap.release()
        self.face_mesh.close()

    ### Diagnosis
    def get_question_and_choices(self) -> tuple[str, list[str] | None]:
        """Get question and choices.

        Returns:
            _type_: question and choices
        """
        assert isinstance(self.mode, DiagnosisMode)
        return self.mode.get_question_and_choices()

    def set_answer(self, answer: int) -> str:
        """Set answer.

        Args:
            answer (_type_): answer

        Returns:
            _type_: message
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)
        if answer == self.mode.CALL_FUNC_ID:
            index_and_choice, _ = self._get_choice_and_effect_diagnosis_func()
            if isinstance(index_and_choice, str):
                return self.mode.SET_ANSWER_ERROR_MSG
            answer = index_and_choice[0]

        return self.mode.set_answer(answer)

    def set_effect_image_by_settings(self):
        """Set effect image by settings."""
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)
        self.mode.set_skin_color(self.skin_hsv)
        self.mode.set_effect_image_by_settings()

    def start_diagnosis_func(self):
        """Start diagnosis func."""
        self._kill_back_process()
        self.back_process = eel.spawn(self._start_diagnosis_func)

    def _start_diagnosis_func(self):
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)

        while True:
            eel.sleep(self.EEL_SLEEP_TIME)
            index_and_choice, effect = self._get_choice_and_effect_diagnosis_func()

            cropped = self._crop_center_x(effect)
            _, imencode_image = cv2.imencode(".jpg", cv2.flip(cropped, 1))
            base64_image = base64.b64encode(imencode_image)
            eel.setVideoSrc("data:image/jpg;base64," + base64_image.decode("ascii"))

            response = index_and_choice if isinstance(index_and_choice, str) else index_and_choice[1].text
            eel.setResult(response)

    def _get_choice_and_effect_diagnosis_func(self) -> tuple[tuple[int, Choice] | str, np.ndarray]:
        """Get choice image diagnosis func.

        Args:
            input_data (_type_): input data
        Returns:
            _type_: choice, effect
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)

        question = self.mode.node.questions[self.mode.child_node_id]
        if question.function == "is_longer_distance_between_eye_than_eye_size":
            image = self._get_image()
            if image is None:
                raise ValueError("failed to get image")

            landmarks = self.face_mesh.get_landmarks(image)
            if landmarks is None:
                return "顔をカメラに向けてください", image

            effect = EyeDiagnosis().render_eye_edge(landmarks, image)
            result = EyeDiagnosis().is_longer_distance_between_eye_than_eye_size(landmarks)
            if result is None:
                return "正面を向いてください", effect
            choice = next((i, choice) for i, choice in enumerate(question.choices) if choice.result == str(result))
            return choice, effect
        else:
            raise ValueError("invalid function")

    ### Custom
    def get_part_kinds(self) -> list[dict]:
        """Get part kinds.

        Returns:
            _type_: part kinds
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, CustomMode)
        return self.mode.get_part_kinds()

    def get_choice_facepaints_by_part(self, part: str) -> list[dict]:
        """Get choice facepaints by part.

        Args:
            part (_type_): part

        Returns:
            _type_: choice facepaints
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, CustomMode)
        return self.mode.get_choice_facepaints_by_part(part)


def main():
    parser = argparse.ArgumentParser(description="iMake!")
    parser.add_argument("--camera_id", type=int, default=0, help="camera id")
    args = parser.parse_args()

    imake = iMake(camera_id=args.camera_id)

    eel.init("i-make/static")
    for attr in dir(imake):
        if callable(getattr(imake, attr)) and not attr.startswith("_"):
            eel.expose(getattr(imake, attr))

    eel.start("dist/index.html", mode="chrome", size=(1920, 1080), port=8080, shutdown_delay=0, block=True)


if __name__ == "__main__":
    main()
