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
        self.blue_yellow = []
        self.summer_winter_judge = []
        self.spring_autumn_judge = []

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
            print("test3")
            self.settings |= node["settings"]
            self.node_id = node["next"]
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

        ##############
        if self.node_id == 8:
            blue_count = self.blue_yellow.count(0)
            yellow_count = self.blue_yellow.count(1)

            if blue_count > yellow_count:
                self.node_id = 9
                return self.SET_ANSWER_SUCCESS_MSG
            else:
                self.node_id = 1
                return self.SET_ANSWER_SUCCESS_MSG
        elif self.node_id > 1 and self.node_id < 9:
            self.node_id = node["choices"][input_data]["next"]
            if node["choices"][input_data]["blue_yellow"] is not None:
                self.blue_yellow.append(node["choices"][input_data]["blue_yellow"])
        #############

        if self.node_id == 15:
            summer_count = self.summer_winter_judge.count(0)
            winter_count = self.summer_winter_judge.count(1)

            if summer_count > winter_count:
                self.node_id = 16
                return self.SET_ANSWER_SUCCESS_MSG
            else:
                self.node_id = 17
                return self.SET_ANSWER_SUCCESS_MSG

        if self.node_id == 26:
            spring_count = self.spring_autumn_judge.count(0)
            winter_count = self.spring_autumn_judge.count(1)

            if spring_count > winter_count:
                self.node_id = 27
                return self.SET_ANSWER_SUCCESS_MSG
            else:
                self.node_id = 28
                return self.SET_ANSWER_SUCCESS_MSG

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
