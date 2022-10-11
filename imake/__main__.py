import argparse
import base64
import time
from dataclasses import asdict
from typing import Any, Final

import cv2
import eel
import numpy as np
from PIL import Image

from .dataclasses import HSV, FacePaint
from .dataclasses.diagnosis import Choice
from .libs.diagnosis import EyeDiagnosis
from .libs.face_detection import FaceDetection
from .libs.facemesh import FaceMesh
from .mode import BaseModeEffectType, ConfigMode, CustomMode, DiagnosisMode, Mode


class IMake:
    EEL_SLEEP_TIME: Final = 0.00000001

    RENDER_IMAGE_WIDTH: Final = 960
    RENDER_IMAGE_HEIGHT: Final = 1080

    def __init__(
        self,
        camera_id: int = 0,
        scale: float = 1.0,
        effect_width: int = 400,
        face_bounding_box_margin: int = 100,
    ) -> None:
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.face_detection = FaceDetection()
        self.cap = cv2.VideoCapture(camera_id)

        self.scale = scale
        self.x_offset = -int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 4)
        self.y_offset = 0

        if effect_width > self.RENDER_IMAGE_WIDTH:
            raise ValueError(
                f"effect_width({effect_width}) must be less than RENDER_IMAGE_WIDTH({self.RENDER_IMAGE_WIDTH})"
            )
        self.EFFECT_WIDTH: Final = effect_width
        self.FACE_BOUNDING_BOX_MARGIN: Final = face_bounding_box_margin

        self.skin_hsv = HSV(h=14, s=36, v=100)
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

    def start_config(self) -> None:
        self._kill_back_process()
        self.mode = ConfigMode()
        image = cv2.imread("imake/static/modes/event/kabuki.png", -1)  # FIXME: hard coding
        self.mode.set_effect_image(image)
        self.back_process = eel.spawn(self._start_rendering())

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
                effect = self._create_effect()
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

    def _create_effect(self, mirror: bool = True) -> np.ndarray:
        """Create effect.

        Returns:
            _type_: effect(BGR)
        """
        try:
            image = self._get_image()
        except Exception as e:
            raise e

        try:
            bounding_box = self.face_detection.get_bounding_box(image)
        except Exception as e:
            raise e

        left = max(0, int(bounding_box.xmin * image.shape[1]) - self.FACE_BOUNDING_BOX_MARGIN)
        right = min(
            int(bounding_box.width * image.shape[1]) + self.FACE_BOUNDING_BOX_MARGIN * 2 + left, image.shape[1]
        )
        top = max(0, int(bounding_box.ymin * image.shape[0]) - self.FACE_BOUNDING_BOX_MARGIN)
        bottom = min(
            int(bounding_box.height * image.shape[0]) + self.FACE_BOUNDING_BOX_MARGIN * 2 + top, image.shape[0]
        )
        face = image[top:bottom, left:right]
        face = cv2.resize(face, (self.EFFECT_WIDTH, int(self.EFFECT_WIDTH * face.shape[0] / face.shape[1])))
        face = cv2.copyMakeBorder(
            face,
            max((self.RENDER_IMAGE_HEIGHT - face.shape[0]) // 2, 0),
            max((self.RENDER_IMAGE_HEIGHT - face.shape[0]) // 2, 0),
            max((self.RENDER_IMAGE_WIDTH - face.shape[1]) // 2, 0),
            max((self.RENDER_IMAGE_WIDTH - face.shape[1]) // 2, 0),
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )

        try:
            landmarks = self.face_mesh.get_landmarks(face)
        except Exception as e:
            raise e

        effect_w_alpha = self.mode.create_effect(face, landmarks)  # type: ignore
        effect = self._convert_rgba_to_rgb(effect_w_alpha)
        scaled = self._scale_image(effect, self.scale)
        translated = self._translate_image(scaled, left + self.x_offset, top + self.y_offset)
        return translated if not mirror else cv2.flip(translated, 1)

    def _convert_rgba_to_rgb(self, image: np.ndarray) -> np.ndarray:
        """Convert RGBA image to RGB image.

        Args:
            image (_type_): RGBA image

        Returns:
            _type_: RGB image
        """
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
        height, width = resized.shape[:2]
        if height > image.shape[0] or width > image.shape[1]:  # 中心を基準に切り取る
            return resized[
                (height - image.shape[0]) // 2 : (height + image.shape[0]) // 2,
                (width - image.shape[1]) // 2 : (width + image.shape[1]) // 2,
            ]
        else:  # 元の画像サイズと同じにする(黒埋め)
            return cv2.copyMakeBorder(
                resized,
                (image.shape[0] - height) // 2,
                (image.shape[0] - height) // 2,
                (image.shape[1] - width) // 2,
                (image.shape[1] - width) // 2,
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

            formatted = self._format_effect(effect, self.scale)
            _, imencode_image = cv2.imencode(".jpg", cv2.flip(formatted, 1))
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
    parser.add_argument("--effect_width", type=int, default=400, help="effect width")
    parser.add_argument(
        "-margin", "--face_bounding_box_margin", type=int, default=100, help="face bounding box margin"
    )
    args = parser.parse_args()

    imake = IMake(
        camera_id=args.camera_id,
        scale=args.scale,
        effect_width=args.effect_width,
        face_bounding_box_margin=args.face_bounding_box_margin,
    )

    eel.init("imake/static")
    for attr in dir(imake):
        if callable(getattr(imake, attr)) and not attr.startswith("_"):
            eel.expose(getattr(imake, attr))

    eel.start("dist/index.html", mode="chrome", size=(1920, 1080), port=8080, shutdown_delay=0, block=True)


if __name__ == "__main__":
    main()
