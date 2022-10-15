import argparse
import base64
import time
from dataclasses import asdict
from typing import Any, Callable, Final

import cv2
import eel
import mediapipe as mp
import numpy as np
from PIL import Image

from .dataclasses import HSV, FacePaint
from .dataclasses.diagnosis import Choice
from .libs.diagnosis import EyeDiagnosis
from .libs.facemesh import FaceMesh
from .libs.palette import PALETTE
from .mode import BaseModeEffectType, ConfigMode, CustomMode, DiagnosisMode, Mode


class IMake:
    EEL_SLEEP_TIME: Final = 0.00000001

    RENDER_IMAGE_WIDTH: Final = 960
    RENDER_IMAGE_HEIGHT: Final = 1080

    def __init__(
        self,
        camera_id: int,
        scale: float,
        effect_width: int,
        face_bounding_box_margin_height: int,
        face_bounding_box_margin_width: int,
        debug: bool,
    ) -> None:
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.face_mesh2 = FaceMesh(refine_landmarks=True)
        self.cap = cv2.VideoCapture(camera_id)
        self.debug = debug

        self.scale = scale
        self.x_offset = -int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 4)
        self.y_offset = 0

        self.EFFECT_WIDTH: Final = effect_width
        self.FACE_BOUNDING_BOX_MARGIN_HEIGHT: Final = face_bounding_box_margin_height
        self.FACE_BOUNDING_BOX_MARGIN_WIDTH: Final = face_bounding_box_margin_width

        self.skin_hsv = PALETTE["skin"][0]
        self.back_process = None

    # Mode
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

    def set_mode(self, mode_name: str, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        """Set mode.

        Args:
            mode_name (_type_): mode name
        """
        self.mode: BaseModeEffectType = Mode[mode_name].value(**kwargs)  # type: ignore

    def get_choice_facepaints(self) -> list[dict]:
        """Get choice facepaints.

        Returns:
            _type_: choice facepaints
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return self.mode.get_choice_facepaints()

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

    # System
    def set_skin_color(self, hsv: dict) -> None:
        """Set skin color.

        Args:
           hue (float, optional): HSVのHueの数値
           sat (float, optional): HSVのSaturationの数値
           val (float, optional): HSVのValueの数値
           include_alpha_ch (bool, optional): setする画像にアルファチャンネルを含むか否か
        """
        self.skin_hsv = HSV(**hsv)
        if self.mode is not None:
            self.mode.set_skin_color(self.skin_hsv, set_as_effect_image=True)

    def update_scale(self, diff: float) -> None:
        """Update scale.

        Args:
            scale (_type_): diff
        """
        self.scale += diff

    def update_x_offset(self, diff: int) -> None:
        """Update x offset.

        Args:
            diff (_type_): diff
        """
        self.x_offset += diff

    def update_y_offset(self, diff: int) -> None:
        """Update y offset.

        Args:
            diff (_type_): diff
        """
        self.y_offset += diff

    def start_skin_color(self) -> None:
        self._kill_back_process()
        self.mode = ConfigMode()  # FIXME ??
        image = cv2.imread(self.mode.SKIN_IMAGE_PATH, -1)
        self.mode.set_effect_image(image)
        self.set_skin_color(asdict(self.skin_hsv))
        self.back_process = eel.spawn(self._start_rendering)

    def start_config(self) -> None:
        self._kill_back_process()
        self.mode = ConfigMode()
        image = cv2.imread(self.mode.ADJUSTMENT_IMAGE_PATH, -1)
        self.mode.set_effect_image(image)
        self.back_process = eel.spawn(self._start_rendering)

    def get_skin_palette(self) -> list[dict]:
        """Get color palette for skin.

        Returns:
            _type_: HSV list
        """
        return [asdict(hsv) for hsv in PALETTE["skin"]]

    def get_config(self) -> dict[str, Any]:
        """Get config.

        Returns:
            _type_: config
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return self.mode.get_class_vars()

    def close(self) -> None:
        self.cap.release()
        self.face_mesh.close()

    # Rendering
    def start_rendering(self) -> None:
        """Start rendering."""
        self._kill_back_process()
        self.back_process = eel.spawn(self._start_rendering)

    def _start_rendering(self) -> None:
        while True:
            eel.sleep(self.EEL_SLEEP_TIME)
            start_time = time.time()

            try:
                image = self._get_image()
            except Exception as e:
                raise e

            try:
                effect = self._create_effect(image, self.mode.create_effect)  # type: ignore
            except Exception as e:
                print(e)
                if self.debug:
                    effect = image
                else:
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

    def _kill_back_process(self) -> None:
        """Kill back process."""
        if self.back_process is not None:
            self.back_process.kill()

    def _get_image(self) -> np.ndarray:
        """Get image.

        Returns:
            _type_: image
        """
        ret, image = self.cap.read()
        if not ret:
            raise Exception("Failed to get image")
        return image

    def _create_effect(self, image: np.ndarray, effect_func: Callable, mirror: bool = True) -> np.ndarray:
        """Create effect.

        Returns:
            _type_: effect(BGR)
        """
        try:
            original_landmarks = self.face_mesh.get_landmarks(image, return_original_style=True)
        except Exception as e:
            raise e

        contour_image = np.zeros(image.shape, dtype=np.uint8)
        mp.solutions.drawing_utils.draw_landmarks(
            image=contour_image,
            landmark_list=original_landmarks,
            connections=mp.solutions.face_mesh.FACEMESH_FACE_OVAL,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=3),
        )
        contours, _ = cv2.findContours(contour_image[:, :, 2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])

        left = max(0, x - self.FACE_BOUNDING_BOX_MARGIN_WIDTH)
        right = min(w + self.FACE_BOUNDING_BOX_MARGIN_WIDTH * 2 + left, image.shape[1])
        top = max(0, y - self.FACE_BOUNDING_BOX_MARGIN_HEIGHT)
        bottom = min(h + self.FACE_BOUNDING_BOX_MARGIN_HEIGHT * 2 + top, image.shape[0])
        face = image[top:bottom, left:right]
        face_effect_width = cv2.resize(
            face, (self.EFFECT_WIDTH, int(self.EFFECT_WIDTH * face.shape[0] / face.shape[1]))
        )

        try:
            landmarks = self.face_mesh2.get_landmarks(face_effect_width)
        except Exception as e:
            raise e

        effect_w_alpha = effect_func(face_effect_width, landmarks)
        effect = self._convert_rgba_to_rgb(effect_w_alpha)
        effect_render_shape = cv2.copyMakeBorder(
            effect,
            max((self.RENDER_IMAGE_HEIGHT - effect.shape[0]) // 2, 0),
            max((self.RENDER_IMAGE_HEIGHT - effect.shape[0]) // 2, 0),
            max((self.RENDER_IMAGE_WIDTH - effect.shape[1]) // 2, 0),
            max((self.RENDER_IMAGE_WIDTH - effect.shape[1]) // 2, 0),
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )
        scaled = self._scale_image(effect_render_shape, self.scale * (right - left) / image.shape[1])
        translated = self._translate_image(scaled, left + self.x_offset, top + self.y_offset)
        return translated if not mirror else cv2.flip(translated, 1)

    def _convert_rgba_to_rgb(self, image: np.ndarray) -> np.ndarray:
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image

        Returns:
            _type_: RGB image
        """
        if image.shape[2] == 3:
            return image
        mask = image[:, :, 3]
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)

    def _scale_image(self, image: np.ndarray, scale: float) -> np.ndarray:
        """The image size is scaled up or down without changing the image size.
        (The areas with no image data are filled in black when the image is
        scaled down.)

        Args:
            image (_type_): image

        Returns:
            _type_: scaled image
        """
        resized = cv2.resize(
            image,
            dsize=None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC,
        )
        resized_height, resized_width = resized.shape[:2]
        if resized_height > image.shape[0] or resized_width > image.shape[1]:  # 中心を基準に切り取る
            return resized[
                (resized_height - image.shape[0]) // 2 : (resized_height - image.shape[0]) // 2 + image.shape[0],
                (resized_width - image.shape[1]) // 2 : (resized_width - image.shape[1]) // 2 + image.shape[1],
            ]
        else:  # 元の画像サイズと同じにする(黒埋め)
            return cv2.copyMakeBorder(
                resized,
                (image.shape[0] - resized_height) // 2,
                (image.shape[0] - resized_height) // 2,
                (image.shape[1] - resized_width) // 2,
                (image.shape[1] - resized_width) // 2,
                cv2.BORDER_CONSTANT,
                value=(0, 0, 0),
            )

    def _translate_image(self, image: np.ndarray, dx: int, dy: int) -> np.ndarray:
        """dx, dyだけ動かしたimageを描画する.

        Args:
            image (_type_): image
            dx (int): x offset
            dy (int): y offset

        Returns:
            _type_: offset image
        """
        offset_image = Image.fromarray(np.zeros((960, 1080, 3), np.uint8))
        offset_image.paste(Image.fromarray(image), (dx, dy))
        return np.array(offset_image).astype(np.uint8)

    # Diagnosis
    def get_question_and_choices(self) -> tuple[str, list[str] | None]:
        """Get question and choices.

        Returns:
            _type_: question and choices
        """
        assert isinstance(self.mode, DiagnosisMode)
        return self.mode.get_question_and_choices()  # type: ignore

    def set_answer(self, answer: int) -> tuple[str, str | None] | str:
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
            index_and_choice = self._get_choice_diagnosis_func()
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
            start_time = time.time()
            index_and_choice = self._get_choice_diagnosis_func()

            try:
                image = self._get_image()
            except Exception as e:
                raise e

            try:
                effect = self._create_effect(image, EyeDiagnosis().render_eye_edge)
            except Exception as e:
                index_and_choice = e.args[0]
                if self.debug:
                    effect = image
                else:
                    effect = image  # FIXME

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

            response = index_and_choice if isinstance(index_and_choice, str) else index_and_choice[1].text
            eel.setResponse(response)

    def _get_choice_diagnosis_func(self) -> tuple[int, Choice] | str:
        """Get choice image diagnosis func.

        Args:
            input_data (_type_): input data
        Returns:
            _type_: choice
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
                return e.args[0]

            try:
                result = EyeDiagnosis().is_longer_distance_between_eye_than_eye_size(landmarks, 1.3)
            except Exception as e:
                return e.args[0]
            choice = next((i, choice) for i, choice in enumerate(question.choices) if choice.result == str(result))
            return choice
        else:
            raise ValueError("invalid function")

    # Custom
    def get_parts(self) -> list[dict]:
        """Get parts.

        Returns:
            _type_: parts
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, CustomMode)
        return self.mode.get_parts()

    def get_choice_facepaints_by_part_name(self, part_name: str) -> list[dict]:
        """Get choice facepaints by part name.

        Args:
            part_name (_type_): part name

        Returns:
            _type_: choice facepaints
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, CustomMode)
        return self.mode.get_choice_facepaints_by_part_name(part_name)

    def get_palette_by_part_name(self, part_name: str) -> list[dict]:
        """Get color palette by part name.

        Args:
            part_name (_type_): part name
        Returns:
            _type_: color palette
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        assert isinstance(self.mode, CustomMode)
        return self.mode.get_palette_by_part_name(part_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="iMake!")
    parser.add_argument("--camera_id", type=int, default=0, help="camera id")
    parser.add_argument("--scale", type=float, default=2.0, help="scale")
    parser.add_argument("--effect_width", type=int, default=400, help="effect width")
    parser.add_argument(
        "-margin_height",
        "--face_bounding_box_margin_height",
        type=int,
        default=100,
        help="face bounding box margin height",
    )
    parser.add_argument(
        "-margin_width",
        "--face_bounding_box_margin_width",
        type=int,
        default=100,
        help="face bounding box margin width",
    )
    parser.add_argument("--debug", action="store_true", help="debug mode if this flag is set (default: False)")
    args = parser.parse_args()

    imake = IMake(
        camera_id=args.camera_id,
        scale=args.scale,
        effect_width=args.effect_width,
        face_bounding_box_margin_height=args.face_bounding_box_margin_height,
        face_bounding_box_margin_width=args.face_bounding_box_margin_width,
        debug=args.debug,
    )

    eel.init("imake/static")
    for attr in dir(imake):
        if callable(getattr(imake, attr)) and not attr.startswith("_"):
            eel.expose(getattr(imake, attr))

    eel.start("dist/index.html", mode="chrome", size=(1920, 1080), port=8080, shutdown_delay=0, block=True)


if __name__ == "__main__":
    main()
