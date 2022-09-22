from enum import Enum, auto
from typing import TypeVar

from .base import BaseModeEffect
from .custom import CustomMode
from .diagnosis import DiagnosisMode
from .easy import EasyMode
from .event import EventMode
from .practice import PracticeMode

BaseModeEffectType = TypeVar("BaseModeEffectType", bound=BaseModeEffect)


class Mode(Enum):
    EVENT = EventMode
    PRACTICE = PracticeMode
    EASY = EasyMode
    DIAGNOSIS = DiagnosisMode
    CUSTOM = CustomMode
