
from abc import abstractmethod
from typing import Self


class RendererSetup:
    def __init__(self: Self) -> None:
        pass

    @abstractmethod
    def init_app(self: Self) -> None:
        pass

    @abstractmethod
    def init_frame(self: Self) -> None:
        pass
