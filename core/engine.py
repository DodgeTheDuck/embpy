
from collections import deque
from asset.asset_shader import AssetShader
from debug.console import Console
import gui.gui as gui
import config
import core.pg as pg
import asset.asset_manager as asset_manager

from core.app_state import AppState
from core.interval_timer import CallbackInterval, Timer
from scene.scene import Scene
import OpenGL.GL as gl

console: Console = None
scene: Scene = None

_app_states: deque[AppState] = deque[AppState]()
_engine_timer: Timer = None
_tick_interval: CallbackInterval = None
_draw_interval: CallbackInterval = None
_impl = None


def init(root_state: AppState) -> None:
    global _engine_timer, _tick_interval, _draw_interval, _impl, console, scene
    console = Console()

    scene = Scene()

    console.write_line("initialising...")
    console.write_line("init pygame")
    pg.init_pygame(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    _app_states.append(root_state)

    console.write_line("load assets...")
    asset_manager.add_asset(AssetShader("basic_shading", "assets/shader/basic_shading.shader").load())
    asset_manager.add_asset(AssetShader("fbo_blit", "assets/shader/fbo_blit.shader").load())
    console.write_line("assets loaded")

    console.write_line("init app")
    root_state.init()

    _engine_timer = Timer()
    _tick_interval = _engine_timer.set_interval(1.0 / config.TPS,
                                                _tick,
                                                "Tick")
    _draw_interval = _engine_timer.set_interval(1.0 / config.FPS,
                                                _draw,
                                                "Draw")
    console.write_line("init GUI")
    gui.init()

    console.write_line("complete")


def run() -> None:
    while pg.handle_window_events(_app_states[-1]):
        _engine_timer.update()


def _tick(delta: int) -> None:
    _app_states[-1].tick(delta)


def _draw(delta: int) -> None:

    # run render pipeline
    while (pg.gl().get_active_pipeline().next()):
        pg.gl().clear()
        _app_states[-1].draw_pass(pg.gl().get_active_pipeline().get_active_stage())

    # finalise pipeline
    pg.gl().get_active_pipeline().end()

    gui.start_frame()
    gui.menu()
    gui.pipeline()
    console.draw_gui()
    pg.gl().get_active_pipeline().draw_gui()
    _app_states[-1].draw_gui()
    asset_manager.draw_gui()
    gui.render()

    pg.swap_buffers()
