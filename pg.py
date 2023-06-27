import pygame

from pygl import Pygl

_window_surface: pygame.surface.Surface = None
_pygl: Pygl = None


def init_pygame(window_width: int, window_height: int) -> None:
    global _window_surface, _pygl
    pygame.init()
    _window_surface = pygame.display.set_mode([window_width, window_height],
                                              pygame.OPENGL | pygame.DOUBLEBUF,
                                              24)
    _pygl = Pygl()
    _pygl.init_gl(window_width, window_height)


def swap_buffers() -> None:
    pygame.display.flip()


def get_window_surface() -> pygame.surface.Surface:
    return _window_surface


def handle_window_events() -> bool:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                return False
    return True


def gl() -> Pygl:
    return _pygl
