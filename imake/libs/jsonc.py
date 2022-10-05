import json
import re
from typing import Any


def load_jsonc(file_path: str) -> dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    re_text = re.sub(r"/\*[\s\S]*?\*/|//.*", "", text)
    json_obj = json.loads(re_text)
    return json_obj
