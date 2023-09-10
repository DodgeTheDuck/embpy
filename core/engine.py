
"""
 Main engine instance.

 PURPOSE: Handles majority of lifetime of application.
"""

from collections import deque
from core.asset.asset_shader import AssetShader
from core.asset.asset_texture import AssetTexture
from debug.console import Console
from core.app_state import AppState
from core.interval_timer import CallbackInterval, Timer
from gfx.gfx import Gfx
from gfx.renderer_setup.renderer_setup_3d import RendererSetup3d
from scene.scene import Scene
import core.asset.asset_manager as asset_manager
import gui.gui as gui
import config
import core.pg as pg

# VARS: sub system

console: Console = None
scene: Scene = None
gfx: Gfx = None

# VARS: private

_app_states: deque[AppState] = deque[AppState]()
_engine_timer: Timer = None
_tick_interval: CallbackInterval = None
_draw_interval: CallbackInterval = None


def init(root_state: AppState) -> None:
    """
    Initialise engine state.

    :param root_state: Bootstrapping app state.
    """

    global _engine_timer, _tick_interval, _draw_interval, console, scene, gfx

    console = Console()
    # init pygame
    console.write_line("initialising...")
    console.write_line("init pygame")
    pg.init_pygame(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    gfx = Gfx(RendererSetup3d())
    console.write_line("initialising gfx...")
    gfx.init_gl()
    console.write_line("initialising gfx complete")

    scene = Scene()

    # load assets NOTE: will be automated at some point
    console.write_line("loading assets...")
    asset_manager.add_asset(AssetShader("basic_shading", "assets/shader/basic_shading.shader").load())
    asset_manager.add_asset(AssetShader("fbo_blit", "assets/shader/fbo_blit.shader").load())
    asset_manager.add_asset(AssetShader("depth_shader", "assets/shader/depth_shader.shader").load())
    asset_manager.add_asset(AssetShader("albedo_only", "assets/shader/albedo_only.shader").load())
    asset_manager.add_asset(AssetShader("skybox", "assets/shader/skybox.shader").load())
    asset_manager.add_asset(AssetTexture("empty_tex", "assets/textures/empty_tex.bmp").load())

    # asset_manager.add_asset(AssetTexture("sky_box_back", "assets/textures/skybox/back.jpg").load())
    # asset_manager.add_asset(AssetTexture("sky_box_front", "assets/textures/skybox/front.jpg").load())
    # asset_manager.add_asset(AssetTexture("sky_box_left", "assets/textures/skybox/left.jpg").load())
    # asset_manager.add_asset(AssetTexture("sky_box_right", "assets/textures/skybox/right.jpg").load())
    # asset_manager.add_asset(AssetTexture("sky_box_bottom", "assets/textures/skybox/bottom.jpg").load())
    # asset_manager.add_asset(AssetTexture("sky_box_top", "assets/textures/skybox/top.jpg").load())

    console.write_line("assets loaded")

    # init engine bootstrapping state
    console.write_line("init app")
    _app_states.append(root_state)
    root_state.init()

    # set up engine timings
    _engine_timer = Timer()
    _tick_interval = _engine_timer.set_interval(1.0 / config.TPS,
                                                _tick,
                                                "Tick")
    _draw_interval = _engine_timer.set_interval(1.0 / config.FPS,
                                                _draw,
                                                "Draw")

    # init GUI
    console.write_line("init GUI")
    gui.init()

    console.write_line("complete")


def run() -> None:
    """
    Begin main engine loop.

    Loop exits when pygame QUIT event is thrown.
    """

    while pg.handle_window_events(_app_states[-1]):
        _engine_timer.update()


def _tick(delta: int) -> None:
    """
    Perform engine/app logic.

    :param delta: Time in seconds since last _tick call
    """

    _app_states[-1].tick(delta)


def _draw(delta: int) -> None:
    """
    Perform engine/app drawing.

    :param delta: Time in seconds since last _draw call
    """

    scene.light_manager.cache_lights()
    scene.camera_manager.cache_cameras()

    gfx.get_active_pipeline().begin()
    scene.camera_manager.apply_cameras()

    # run render pipeline
    while (gfx.get_active_pipeline().next()):
        gfx.get_active_pipeline().get_active_stage().begin_state()
        gfx.clear()
        _app_states[-1].draw_pass(gfx.get_active_pipeline().get_active_stage_index())
        gfx.get_active_pipeline().get_active_stage().end_state()

    scene.camera_manager.end_cameras()
    # finalise pipeline
    gfx.get_active_pipeline().end()

    # render GUI
    gui.start_frame()
    gui.menu()
    console.draw_gui()
    gfx.get_active_pipeline().draw_gui()
    _app_states[-1].draw_gui()
    asset_manager.draw_gui()
    gui.render()

    # display current frame
    pg.swap_buffers()
