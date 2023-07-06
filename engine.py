
from collections import deque
import sys
from typing import Self

import pygame

import config
import pg
from imgui.integrations.opengl import ProgrammablePipelineRenderer
import imgui

from app_state import AppState
from interval_timer import CallbackInterval, Timer

_app_states: deque[AppState] = deque[AppState]()
_engine_timer: Timer = None
_tick_interval: CallbackInterval = None
_draw_interval: CallbackInterval = None
_impl = None


def init(root_state: AppState) -> None:
    global _engine_timer, _tick_interval, _draw_interval, _impl
    pg.init_pygame(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    _app_states.append(root_state)

    root_state.init()

    _engine_timer = Timer()
    _tick_interval = _engine_timer.set_interval(1.0 / config.TPS,
                                                _tick,
                                                "Tick")
    _draw_interval = _engine_timer.set_interval(1.0 / config.FPS,
                                                _draw,
                                                "Draw")
    imgui.create_context()
    _impl = ProgrammablePipelineRenderer()
    _impl.io.display_size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)


def run() -> None:
    while pg.handle_window_events(_app_states[-1]):
        _engine_timer.update()


def _tick(delta: int) -> None:
    _app_states[-1].tick(delta)


def _draw(delta: int) -> None:

    pg.gl().clear()
    _app_states[-1].draw(delta)

    imgui.new_frame()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", "Cmd+Q", False, True
            )

            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()

    imgui.render()

    _impl.render(imgui.get_draw_data())

    pg.swap_buffers()
