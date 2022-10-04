from pydantic.dataclasses import dataclass


@dataclass
class Choice:
    text: str
    answer_id: str
    next_node_id: str | int | None
    result: str | None = None  # function call result


@dataclass
class Question:
    text: str
    choices: list[Choice]
    function: str | None = None


@dataclass
class Answer:
    next_node_id: str | None
    settings: dict[str, str | tuple[float, float, float]]
    count: int = 0


@dataclass
class Node:
    questions: dict[str, Question]
    answers: dict[str, Answer]
    category: str | None = None
