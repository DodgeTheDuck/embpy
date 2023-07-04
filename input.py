
from typing import Self

import pygame


class Mouse:
    def __init__(self: Self) -> None:
        self.x = 0
        self.y = 0
        self.delta_x = 0
        self.delta_y = 0


__mouse: Mouse = Mouse()


def handle_event(event: pygame.Event) -> None:
    match event.type:
        case pygame.MOUSEMOTION:
            __mouse.delta_x = event.rel[0]
            __mouse.delta_y = event.rel[1]
            __mouse.x = event.pos[0]
            __mouse.y = event.pos[1]


def mouse() -> Mouse:
    return __mouse
