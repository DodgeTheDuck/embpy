
from abc import ABC, abstractmethod
from typing import Self


class AppState(ABC):

    @abstractmethod
    def init(self: Self) -> None:
        pass

    @abstractmethod
    def tick(self: Self, delta_ns: int) -> None:
        pass

    @abstractmethod
    def draw(self: Self, delta_ns: int) -> None:
        pass
