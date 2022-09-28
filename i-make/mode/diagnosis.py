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
    DATA_PATH: str = "i-make/static/facepaints/diagnosis/data.jsonc"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def diagnosis(cls):
        """どの画像を重ね合わせるべきか診断する."""
        data = load_jsonc(cls.DATA_PATH)
        node_id = 1
        settings = {}

        while True:
            node = data[str(node_id)]
            if node["question"] is not None:
                print(node["question"])

                for i, choice in enumerate(node["choices"]):
                    print(f"{i + 1}: {choice['answer']}")
                input_data = input(">> ")
                if not (input_data in [str(i + 1) for i in range(len(node["choices"]))]):
                    print("選択肢にある数字を入力してください")
                    continue
                node_id = node["choices"][int(input_data) - 1]["next"]
            else:
                if node["settings"] is None:
                    print("診断終了")
                    break
                settings |= node["settings"]
                node_id = node["next"]
        print(settings)
