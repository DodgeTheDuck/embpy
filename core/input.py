"""
Pygame input wrapper.

PURPOSE: Expose various input input states to application
"""

from typing import Self
import pygame


class Mouse:
    """
    Current mouse state.

    NOTE: Updated during window event handler
    """
    def __init__(self: Self) -> None:
        self.x = 0
        self.y = 0
        self.delta_x = 0
        self.delta_y = 0


# VARS: private
_mouse: Mouse = Mouse()


def handle_event(event: pygame.Event) -> None:
    """
    Check for input event. Update state accordingly.

    :param event: Event to handle.
    """
    match event.type:
        case pygame.MOUSEMOTION:
            _mouse.delta_x = event.rel[0]
            _mouse.delta_y = event.rel[1]
            _mouse.x = event.pos[0]
            _mouse.y = event.pos[1]


def mouse() -> Mouse:
    return _mouse
