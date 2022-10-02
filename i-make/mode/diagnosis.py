import json
import re

from ..mode.base import BaseModeEffect


def load_jsonc(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    re_text = re.sub(r"/\*[\s\S]*?\*/|//.*", "", text)
    json_obj = json.loads(re_text)
    return json_obj


class DiagnosisMode(BaseModeEffect):
    """Diagnosis makeup mode."""

    ICON_PATH: str = "i-make/static/facepaints/diagnosis/diagnosis.png"
    DATA_PATH: str = "i-make/static/facepaints/diagnosis/data_test.jsonc"

    SET_ANSWER_SUCCESS_MSG = "Success."
    SET_ANSWER_ERROR_MSG = "Invalid input."
    DIAGNOSIS_FINISH_MSG = "診断終了"

    DEFAULT_HSV = [0, 0, 0]

    def __init__(self, *args, **kwargs) -> None:
        self.data = load_jsonc(self.DATA_PATH)
        self.node_id = 1
        self.settings = {}
        self.blue_yellow = [0]
        self.blue_summer_winter = [0]
        self.yellow_spring_autumn = [0]
        super().__init__(*args, **kwargs)

    def get_question_and_choices(self) -> tuple[str, dict[str, str | int]]:
        """Get question and choices."""
        node = self.data[str(self.node_id)]

        if node["question"] is not None:
            return node["question"], node["choices"]

        if node["settings"] is None:
            self.set_skin_color(14, 36, 100)
            self._set_effect_image_by_settings()
            return self.DIAGNOSIS_FINISH_MSG, {}
        else:
            self.settings |= node["settings"]
            self.node_id = node["next"]

            if node["blue_yellow"] is not None:
                self.blue_yellow.appened(node["blue_yellow"])

            if node["blue_yellow_judge"] is not None:
                blue_count = self.blue_yellow.count(0)
                yellow_count = self.blue_yellow.count(1)

                if blue_count > yellow_count:
                    self.node_id = 3  # TODO 適当な数字入れる、下も同様
                elif blue_count < yellow_count:
                    self.node_id = 3
                else:
                    self.node_id = 3

            if node["blue_summer_winter"] is not None:
                self.blue_summer_winter.append(node["blue_summer_winter"])

            if node["blue_summer_winter_judge"] is not None:
                summer_count = self.blue_summer_winter.count(0)
                winter_count = self.blue_summer_winter.count(1)

                if summer_count > winter_count:
                    self.node_id = 3
                elif summer_count < winter_count:
                    self.node_id = 3
                else:
                    self.node_id = 3

            if node["yellow_spring_autumn"] is not None:
                self.yellow_spring_autumn.append(node["yellow_sprint_autumn"])

            if node["yellow_spring`_autumn_judge"] is not None:
                spring_count = self.yellow_spring_autumn.count(0)
                autumn_count = self.yellow_spring_autumn.count(1)

                if spring_count > autumn_count:
                    self.node_id = 3
                elif spring_count < autumn_count:
                    self.node_id = 3
                else:
                    self.node_id = 3

            return self.get_question_and_choices()

    def set_answer(self, input_data: int) -> str:
        """Set answer.

        Args:
            input_data (int): Input data (choices 0 index).

        Returns:
            str: Message.
        """
        node = self.data[str(self.node_id)]
        if not (0 <= input_data < len(node["choices"])):
            return self.SET_ANSWER_ERROR_MSG
        self.node_id = node["choices"][input_data]["next"]
        return self.SET_ANSWER_SUCCESS_MSG

    def _set_effect_image_by_settings(self) -> None:
        path_list = []
        hsv_list = []
        for key, value in self.settings.items():
            if "color" in key:
                continue
            path_list.append(value)
            hsv_list.append(self.settings[key + "-color"] if self.settings.get(key + "-color") else self.DEFAULT_HSV)
        self.set_effect_image_from_path_w_hsv(path_list, hsv_list)
