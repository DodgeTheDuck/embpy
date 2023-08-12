
from collections import deque
from debug.console import Console
import gui.gui as gui
import config
import core.pg as pg
import OpenGL.GL as gl

from core.app_state import AppState
from core.interval_timer import CallbackInterval, Timer
from scene.scene import Scene
from scene.scene_object import SceneObjectType

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

    pg.gl().bind_pipeline_stage("geometry")
    pg.gl().clear_color(0, 0, 0)
    pg.gl().clear()
    pg.gl().bind_active_pipeline_stage_shader()
    _app_states[-1].draw_geometry()

    pg.gl().bind_pipeline_stage("light_pass")
    pg.gl().clear_color(0, 0, 0)
    pg.gl().clear()
    pg.gl().bind_active_pipeline_stage_shader()
    _app_states[-1].draw_camera()  # NOTE: temporary until i work out how to handle cameras better
    pg.gl().pipeline.bind_textures("geometry", pg.gl().get_active_pipeline_stage().draw_shader)
    _app_states[-1].draw_lighting()

    pg.gl().bind_pipeline_stage("shading")
    pg.gl().bind_active_pipeline_stage_shader()
    pg.gl().pipeline.blit_stage("light_pass")

    # pg.gl().bind_pipeline_stage("shading")
    # pg.gl().bind_active_pipeline_stage_shader()
    # _app_states[-1].draw_camera()
    # pg.gl().pipeline.bind_textures("geometry", pg.gl().pipeline.stages["shading"].draw_shader)
    # pg.gl().pipeline.draw_stage("shading")
    # pg.gl().bind_default_framebuffer()
    # pg.gl().pipeline.blit_stage("shading")

    gui.start_frame()
    gui.menu()
    gui.pipeline()
    console.gui()
    _app_states[-1].gui()
    gui.render()

    pg.swap_buffers()
