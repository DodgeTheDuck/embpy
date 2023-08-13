
from abc import abstractmethod
from enum import Enum
from typing import Self


class AssetType(Enum):
    NONE = 0
    SHADER = 1


class Asset:
    def __init__(self: Self, name: str, type: AssetType) -> None:
        self.name = name
        self.type = type
        self.loaded = False
        self.object = None
        pass

    @abstractmethod
    def load(self: Self) -> Self:
        pass

    @abstractmethod
    def draw_gui(self: Self) -> None:
        pass
