import argparse
import base64
import time

import cv2
import eel
import numpy as np

from .libs.facemesh import FaceMesh
from .mode import BaseModeEffectType, DiagnosisMode, Mode


class iMake:
    def __init__(self, camera_id: int = 0):
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.cap = cv2.VideoCapture(camera_id)

    def set_mode(self, mode_name: str, *args, **kwargs):
        """Set mode.

        Args:
            mode_name (_type_): mode name
        """
        self.mode: BaseModeEffectType = Mode[mode_name].value(**kwargs)

    def get_mode_choices(self) -> list[dict[str, str]]:
        """Get mode choices."""
        return [
            {"name": mode.name, "icon_path": "../" + mode.value.ICON_PATH.replace("i-make/static/", "")}
            for mode in Mode
        ]

    def set_effect_image_from_path(self, effect_image_path: list[str] | str) -> None:
        """Set effect image from path.

        Args:
            effect_image_path (_type_): path to effect image
        """
        if isinstance(effect_image_path, str):
            effect_image_path = [effect_image_path]

        effect_image_path = ["i-make/static/" + path.replace("../", "") for path in effect_image_path]
        if self.mode is None:
            raise ValueError("mode is not set")
        self.mode.set_effect_image_from_path(effect_image_path)

    def set_skin_color(self, hue: float, sat: float, val: float):
        """Set skin color.

        Args:
           hue (float, optional): HSVのHueの数値 (o%~100%)
           sat (float, optional): HSVのSaturationの数値 (o%~100%)
           val (float, optional): HSVのVvalueの数値 (o%~100%)
           include_alpha_ch (bool, optional): setする画像にアルファチャンネルを含むか否か
        """
        if self.mode is None:
            raise ValueError("mode is not set")

        self.mode.set_skin_color(hue, sat, val)

    def get_choice_images(self) -> list[str]:
        """Get choice images.

        Returns:
            _type_: choice images
        """
        if self.mode is None:
            raise ValueError("mode is not set")
        return ["../" + file.replace("i-make/static/", "") for file in self.mode.get_choice_images_paths()]

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

        effect_w_alpha = self.mode.create_effect(image, landmarks)
        effect = self._convert_rgba_to_rgb(effect_w_alpha)
        cropped = self._crop_center_x(effect)
        return cv2.flip(cropped, 1) if mirror else cropped

    def start(self):
        while True:
            start_time = time.time()
            eel.sleep(0.000001)
            effect = self._process()
            if effect is None:
                continue

            _, imencode_image = cv2.imencode(".jpg", effect)
            base64_image = base64.b64encode(imencode_image)
            eel.setBase64Image("data:image/jpg;base64," + base64_image.decode("ascii"))

            elapsed_time = round((time.time() - start_time), 3)
            eel.setFPS(1 / 1 / elapsed_time)

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

    def close(self):
        self.cap.release()
        self.face_mesh.close()

    ### Diagnosis
    def get_question_and_choices(self):
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
        return self.mode.set_answer(answer)


def main():
    parser = argparse.ArgumentParser(description="iMake!")
    parser.add_argument("--camera_id", type=int, default=0, help="camera id")
    args = parser.parse_args()

    imake = iMake(camera_id=args.camera_id)

    eel.init("i-make/static")
    eel.expose(imake.set_mode)
    eel.expose(imake.get_mode_choices)
    eel.expose(imake.set_effect_image_from_path)
    eel.expose(imake.start)
    eel.expose(imake.get_choice_images)
    eel.expose(imake.set_skin_color)
    eel.expose(imake.get_config)
    eel.expose(imake.get_question_and_choices)
    eel.expose(imake.set_answer)
    eel.start("dist/index.html", mode="chrome", size=(1920, 1080), port=8082, shutdown_delay=0, block=True)


if __name__ == "__main__":
    main()
