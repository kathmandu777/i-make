from typing import Any


def get_index(l: list, x: Any, default: Any = None) -> Any:
    return l.index(x) if x in l else default
