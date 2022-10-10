import argparse
import base64
import time
from dataclasses import asdict
from typing import Any, Final

import cv2
import eel
import numpy as np

from .dataclasses import HSV, FacePaint
from .dataclasses.diagnosis import Choice
from .libs.diagnosis import EyeDiagnosis
from .libs.facemesh import FaceMesh
from .mode import BaseModeEffectType, CustomMode, DiagnosisMode, Mode


class IMake:
    EEL_SLEEP_TIME: Final = 0.00000001

    def __init__(self, camera_id: int = 0, scale: float = 1.0) -> None:
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.cap = cv2.VideoCapture(camera_id)
        self.scale = scale

        self.skin_hsv = HSV(h=14, s=36, v=100)
        self.back_process = None

    def set_mode(self, mode_name: str, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        """Set mode.

        Args:
            mode_name (_type_): mode name
        """
        self.mode: BaseModeEffectType = Mode[mode_name].value(**kwargs)  # type: ignore

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

    def set_effect_image_by_facepaints(self, facepaints: list[dict] | dict) -> None:
        """Set effect image by facepaints.

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

    def set_skin_color(self, hsv: dict) -> None:
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

    def _process(self, mirror: bool = True) -> np.ndarray:
        """Process.

        Returns:
            _type_: effect(BGR)
        """
        try:
            image = self._get_image()
        except Exception as e:
            raise e

        try:
            landmarks = self.face_mesh.get_landmarks(image)
        except Exception as e:
            raise e

        effect_w_alpha = self.mode.create_effect(image, landmarks)  # type: ignore
        effect = self._convert_rgba_to_rgb(effect_w_alpha)
        cropped = self._crop_and_zoom(effect, self.scale)
        return cv2.flip(cropped, 1) if mirror else cropped

    def start(self) -> None:
        """Start."""
        self._kill_back_process()
        self.back_process = eel.spawn(self._start)

    def _start(self) -> None:
        while True:
            eel.sleep(self.EEL_SLEEP_TIME)
            start_time = time.time()
            try:
                effect = self._process()
            except Exception as e:
                print(e)
                continue

            cv2.putText(
                effect,
                "FPS: {:.2f}".format(1.0 / (time.time() - start_time)),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                thickness=2,
            )
            _, imencode_image = cv2.imencode(".jpg", effect)
            base64_image = base64.b64encode(imencode_image)
            eel.setVideoSrc("data:image/jpg;base64," + base64_image.decode("ascii"))

    def stop(self) -> None:
        self._kill_back_process()
        eel.setVideoSrc("/dist/guide.png")  # FIXME

    def _get_image(self) -> np.ndarray:
        """Get image.

        Returns:
            _type_: image
        """
        ret, image = self.cap.read()
        if not ret:
            raise Exception("Failed to get image")
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

    def _crop_and_zoom(self, image: np.ndarray, zoom: float = 1.0) -> np.ndarray:
        """Crop and zoom.

        Args:
            image (_type_): image
            zoom (float, optional): zoom

        Returns:
            _type_: cropped and zoomed image
        """
        cropped_image = self._crop_center_x(image)
        zoomed_image = cv2.resize(cropped_image, None, fx=zoom, fy=zoom)
        return self._trim_center(zoomed_image, cropped_image.shape[1], cropped_image.shape[0])

    def _crop_center_x(self, image: np.ndarray) -> np.ndarray:
        """Crop center x.

        Args:
            image (_type_): image

        Returns:
            _type_: image
        """
        return image[:, image.shape[1] // 4 : image.shape[1] * 3 // 4, :]

    def _trim_center(self, img: np.ndarray, width: int, height: int) -> np.ndarray:
        h, w = img.shape[:2]
        top = int((h / 2) - (height / 2))
        bottom = top + height
        left = int((w / 2) - (width / 2))
        right = left + width
        return img[top:bottom, left:right]

    def get_config(self) -> dict[str, Any]:
        """Get config.

        Returns:
            _type_: config
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return self.mode.get_class_vars()

    def _kill_back_process(self) -> None:
        """Kill back process."""
        if self.back_process is not None:
            self.back_process.kill()

    def close(self) -> None:
        self.cap.release()
        self.face_mesh.close()

    # Diagnosis
    def get_question_and_choices(self) -> tuple[str, list[str] | None]:
        """Get question and choices.

        Returns:
            _type_: question and choices
        """
        assert isinstance(self.mode, DiagnosisMode)
        return self.mode.get_question_and_choices()  # type: ignore

    def set_answer(self, answer: int) -> tuple[str, dict[str, str] | None]:
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

    def set_effect_image_by_settings(self) -> None:
        """Set effect image by settings."""
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)
        self.mode.set_skin_color(self.skin_hsv)
        self.mode.set_effect_image_by_settings()

    def start_diagnosis_func(self) -> None:
        """Start diagnosis func."""
        self._kill_back_process()
        self.back_process = eel.spawn(self._start_diagnosis_func)

    def _start_diagnosis_func(self) -> None:
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, DiagnosisMode)

        while True:
            eel.sleep(self.EEL_SLEEP_TIME)
            index_and_choice, effect = self._get_choice_and_effect_diagnosis_func()

            cropped = self._crop_and_zoom(effect, self.scale)
            _, imencode_image = cv2.imencode(".jpg", cv2.flip(cropped, 1))
            base64_image = base64.b64encode(imencode_image)
            eel.setVideoSrc("data:image/jpg;base64," + base64_image.decode("ascii"))

            response = index_and_choice if isinstance(index_and_choice, str) else index_and_choice[1].text
            eel.setResponse(response)

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
        if question.function == "is_longer_distance_between_eye_than_eye_size":  # FIXME: hard coding
            image = self._get_image()

            try:
                landmarks = self.face_mesh.get_landmarks(image)
            except Exception as e:
                return e.args[0], image

            effect = EyeDiagnosis().render_eye_edge(landmarks, image, do_overlay=False)
            try:
                result = EyeDiagnosis().is_longer_distance_between_eye_than_eye_size(landmarks, 1.3)
            except Exception as e:
                return e.args[0], effect
            choice = next((i, choice) for i, choice in enumerate(question.choices) if choice.result == str(result))
            return choice, effect
        else:
            raise ValueError("invalid function")

    # Custom
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


def main() -> None:
    parser = argparse.ArgumentParser(description="iMake!")
    parser.add_argument("--camera_id", type=int, default=0, help="camera id")
    parser.add_argument("--scale", type=float, default=1.0, help="scale")
    args = parser.parse_args()

    imake = IMake(camera_id=args.camera_id, scale=args.scale)

    eel.init("imake/static")
    for attr in dir(imake):
        if callable(getattr(imake, attr)) and not attr.startswith("_"):
            eel.expose(getattr(imake, attr))

    eel.start("dist/index.html", mode="chrome", size=(1920, 1080), port=8080, shutdown_delay=0, block=True)


if __name__ == "__main__":
    main()
