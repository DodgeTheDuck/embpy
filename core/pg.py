import pygame
from core.app_state import AppState
import core.input as input
import gui.gui as gui
import core.engine as engine

_window_surface: pygame.surface.Surface = None


def init_pygame(window_width: int, window_height: int) -> None:
    global _window_surface, _pygl
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 6)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                    pygame.GL_CONTEXT_PROFILE_CORE)

    engine.console.write_line(f"creating display: {window_width, window_height}")

    _window_surface = pygame.display.set_mode([window_width, window_height],
                                              pygame.OPENGL | pygame.DOUBLEBUF,
                                              24)


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
