from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class RGB:
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

    def __str__(self) -> str:
        return f"RGB({self.r}, {self.g}, {self.b})"


@dataclass
class HSV:
    h: float = Field(..., ge=0, le=360)
    s: float = Field(..., ge=0, le=100)
    v: float = Field(..., ge=0, le=100)

    def __str__(self) -> str:
        return f"HSV({self.h}, {self.s}%, {self.v}%)"
