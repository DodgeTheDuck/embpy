
from collections import deque

import config
import pg


from app_state import AppState
from interval_timer import CallbackInterval, Timer

_app_states: deque[AppState] = deque[AppState]()
_engine_timer: Timer = None
_tick_interval: CallbackInterval = None
_draw_interval: CallbackInterval = None


def init(root_state: AppState) -> None:
    global _engine_timer, _tick_interval, _draw_interval
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


def run() -> None:
    while pg.handle_window_events(_app_states[-1]):
        _engine_timer.update()


def _tick(delta: int) -> None:
    _app_states[-1].tick(delta)


def _draw(delta: int) -> None:
    pg.gl().clear()
    _app_states[-1].draw(delta)
    pg.swap_buffers()
