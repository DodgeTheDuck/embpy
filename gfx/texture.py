
from abc import abstractmethod
from typing import Self


class Texture:
    def __init__(self: Self) -> None:
        self.texture = 0

    @abstractmethod
    def bind(self: Self, index: int) -> None:
        pass
