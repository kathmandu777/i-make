import argparse
import base64
from dataclasses import asdict

import cv2
import eel
import numpy as np

from .dataclasses import HSV, FacePaint
from .libs.facemesh import FaceMesh
from .mode import BaseModeEffectType, CustomMode, DiagnosisMode, Mode


class iMake:
    def __init__(self, camera_id: int = 0):
        self.face_mesh = FaceMesh(refine_landmarks=True)
        self.cap = cv2.VideoCapture(camera_id)

        self.skin_hsv = HSV(h=14, s=36, v=100)
        self.update_image = False

    def set_mode(self, mode_name: str, *args, **kwargs):
        """Set mode.

        Args:
            mode_name (_type_): mode name
        """
        self.mode: BaseModeEffectType = Mode[mode_name].value(**kwargs)

    def get_mode_choices(self) -> list[dict[str, str]]:
        """Get mode choices."""
        return [{"name": mode.name, "icon_path": mode.value.icon_path_for_frontend()} for mode in Mode]

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
        palette = [HSV(h=14, s=36, v=100), HSV(h=27, s=36, v=100)]
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
        self.update_image = True
        while self.update_image:
            eel.sleep(0.000000001)
            effect = self._process()
            if effect is None:
                continue

            _, imencode_image = cv2.imencode(".jpg", effect)
            base64_image = base64.b64encode(imencode_image)
            eel.setVideoSrc("data:image/jpg;base64," + base64_image.decode("ascii"))

    def stop(self):
        self.update_image = False

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
