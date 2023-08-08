
from abc import ABC, abstractmethod
from typing import Self

import pygame


class AppState(ABC):

    @abstractmethod
    def init(self: Self) -> None:
        pass

    @abstractmethod
    def tick(self: Self, delta: int) -> None:
        pass

    @abstractmethod
    def draw_geometry(self: Self) -> None:
        pass

    @abstractmethod
    def draw_lighting(self: Self) -> None:
        pass

    @abstractmethod
    def draw_camera(self: Self) -> None:
        pass

    @abstractmethod
    def gui(self: Self) -> None:
        pass

    @abstractmethod
    def event(self: Self, event: pygame.Event) -> None:
        pass
