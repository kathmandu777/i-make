import re
from typing import Any, Final

import yaml

from ..dataclasses import HSV, FacePaint
from ..dataclasses.diagnosis import Node
from ..mode.base import BaseModeEffect


class DiagnosisMode(BaseModeEffect):
    """Diagnosis makeup mode."""

    ICON_PATH: str = "imake/static/modes/diagnosis/icon.png"
    MENU_IMAGE_PATH: str = "imake/static/modes/diagnosis/menu.png"

    DATA_PATH: Final = "imake/static/modes/diagnosis/data.yml"
    FIRST_NODE_ID: Final = "1"

    SET_ANSWER_SUCCESS_MSG: Final = "Success."
    SET_ANSWER_ERROR_MSG: Final = "Invalid input."
    DIAGNOSIS_FINISH_MSG: Final = "診断終了"

    SUB_HSV_DIFF: Final = (0.0, 25.0, -10.0)

    CALL_FUNC_ID: Final = -1

    def __init__(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> None:
        with open(self.DATA_PATH, "r") as f:
            self.data = yaml.safe_load(f)

        self.node = Node(**self.data[self.FIRST_NODE_ID])
        self.child_node_id = self.FIRST_NODE_ID
        self.settings: dict[str, Any] = {}
        self.results: dict[str, Any] = {}
        super().__init__(*args, **kwargs)

    def get_question_and_choices(self) -> tuple[str, list[str] | None]:
        """Get question and choices.

        Returns:
            tuple[str, list[str]]: Question and choices.
        """
        question = self.node.questions[self.child_node_id]
        if question.function is not None:
            choices = None
        else:
            choices = [choice.text for choice in question.choices]
        return question.text, choices

    def set_answer(self, input_data: int) -> tuple[str, dict[str, str] | None]:
        """Set answer.

        Args:
            input_data (int): Input data (choices 0 index).

        Returns:
            _type_: Message and results.
        """
        if not (0 <= input_data < len(self.node.questions[self.child_node_id].choices)):
            return self.SET_ANSWER_ERROR_MSG, None

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
                    if value not in self.settings[key]:
                        self.settings[key].append(value)

            category_or_question = self.node.category or self.node.questions[self.FIRST_NODE_ID].text
            self.results[category_or_question] = self.node.answers[max_answer_id].label

            next_node_id = self.node.answers[max_answer_id].next_node_id

            if next_node_id is None:  # 診断終了
                return self.DIAGNOSIS_FINISH_MSG, self.results

            # 次のカテゴリの質問へ
            self.node = Node(**self.data[str(next_node_id)])
            self.child_node_id = self.FIRST_NODE_ID
            return self.SET_ANSWER_SUCCESS_MSG, None

        # カテゴリ内の次の質問へ
        self.child_node_id = str(answer.next_node_id)
        return self.SET_ANSWER_SUCCESS_MSG, None

    def set_effect_image_by_settings(self) -> None:
        """Set effect image by settings."""
        facepaints = []
        for key, values in self.settings.items():
            if "color" in key:
                continue

            if not (f'{key.replace("-sub","")}-color' in self.settings.keys()):
                hsv = None
            else:
                color: tuple[float, float, float] = self.settings[(f'{key.replace("-sub","")}-color')]
                if "-sub" in key:
                    color = tuple([x + y for x, y in zip(color, self.SUB_HSV_DIFF)])  # type: ignore # FIXME
                hsv = HSV(h=color[0], s=color[1], v=color[2])

            for value in values:
                dir_path, filename = value.rsplit("/", 1)
                facepaints.append(FacePaint(filename=filename, image_dir_path=dir_path, hsv=hsv))

        self.set_effect_image_by_facepaints(facepaints)
