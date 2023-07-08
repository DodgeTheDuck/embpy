import pygame
from app_state import AppState
import input
from gl.pygl import Pygl
import gui

_window_surface: pygame.surface.Surface = None
_pygl: Pygl = None


def init_pygame(window_width: int, window_height: int) -> None:
    global _window_surface, _pygl
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 6)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                    pygame.GL_CONTEXT_PROFILE_CORE)

    _window_surface = pygame.display.set_mode([window_width, window_height],
                                              pygame.OPENGL | pygame.DOUBLEBUF,
                                              24)
    _pygl = Pygl()
    _pygl.init_gl(window_width, window_height)


def swap_buffers() -> None:
    pygame.display.flip()


def get_window_surface() -> pygame.surface.Surface:
    return _window_surface


def handle_window_events(app_state: AppState) -> bool:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                return False
        input.handle_event(event)
        gui.handle_event(event)
        app_state.event(event)
    return True


def gl() -> Pygl:
    return _pygl
