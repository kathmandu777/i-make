import json
import re

from ..dataclasses import HSV, FacePaint
from ..dataclasses.diagnosis import Node
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

    DATA_PATH: str = "i-make/static/facepaints/diagnosis/data.jsonc"
    FIRST_NODE_ID: str = "first"
    FIRST_CHILD_NODE_ID: str = "1"

    SET_ANSWER_SUCCESS_MSG = "Success."
    SET_ANSWER_ERROR_MSG = "Invalid input."
    DIAGNOSIS_FINISH_MSG = "診断終了"

    DEFAULT_HSV = HSV(h=0, s=0, v=0)
    SUB_HSV_DIFF = (0.0, 25.0, -10.0)

    def __init__(self, *args, **kwargs) -> None:
        self.data = load_jsonc(self.DATA_PATH)
        self.node = Node(**self.data[self.FIRST_NODE_ID])
        self.child_node_id = self.FIRST_CHILD_NODE_ID
        self.settings = {}
        super().__init__(*args, **kwargs)

    def get_question_and_choices(self) -> tuple[str, list[str]]:
        """Get question and choices.

        Returns:
            tuple[str, list[str]]: Question and choices.
        """
        question = self.node.questions[self.child_node_id]
        choices = [choice.text for choice in question.choices]
        return question.text, choices

    def set_answer(self, input_data: int) -> str:
        """Set answer.

        Args:
            input_data (int): Input data (choices 0 index).

        Returns:
            str: Message.
        """
        if not (0 <= input_data < len(self.node.questions[self.child_node_id].choices)):
            return self.SET_ANSWER_ERROR_MSG

        answer = self.node.questions[self.child_node_id].choices[input_data]
        self.node.answers[answer.answer_id].count += 1

        if answer.next_node_id is None:  # そのカテゴリの質問が終了
            max_answer_id = max(self.node.answers.items(), key=lambda x: x[1].count)[0]
            for key, value in self.node.answers[max_answer_id].settings.items():
                key = re.sub(r"[0-9]", "", key)
                if self.settings.get(key) is None:
                    if "color" in key:
                        self.settings[key] = value
                    else:
                        self.settings[key] = [value]
                else:
                    self.settings[key].append(value)
            next_node_id = self.node.answers[max_answer_id].next_node_id

            if next_node_id is None:  # 診断終了
                return self.DIAGNOSIS_FINISH_MSG

            # 次のカテゴリの質問へ
            self.node = Node(**self.data[str(next_node_id)])
            self.child_node_id = self.FIRST_CHILD_NODE_ID
            return self.SET_ANSWER_SUCCESS_MSG

        # カテゴリ内の次の質問へ
        self.child_node_id = str(answer.next_node_id)
        return self.SET_ANSWER_SUCCESS_MSG

    def set_effect_image_by_settings(self) -> None:
        """Set effect image by settings."""
        facepaints = []
        for key, values in self.settings.items():
            if "color" in key:
                continue

            for value in values:
                dir_path, filename = value.rsplit("/", 1)

                color: tuple[float, float, float] | None = self.settings.get(f'{key.replace("-sub","")}-color')
                if color is None:
                    hsv = self.DEFAULT_HSV
                else:
                    if "-sub" in key:
                        print(color, self.SUB_HSV_DIFF)
                        color = tuple([x + y for x, y in zip(color, self.SUB_HSV_DIFF)])
                    hsv = HSV(h=color[0], s=color[1], v=color[2])

                facepaints.append(FacePaint(filename=filename, image_dir_path=dir_path, hsv=hsv))

        self.set_effect_image_by_facepaints(facepaints)
