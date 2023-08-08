
from typing import Self


class Rect:
    def __init__(self: Self, left: float, top: float,
                 width: float, height: float) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
