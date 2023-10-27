
import core.engine as engine
import OpenGL.GL as gl
import config

from typing import Self
from gfx.renderer_setup.renderer_setup import RendererSetup


class RendererSetup3d(RendererSetup):
    def __init__(self: Self) -> None:
        super().__init__()

    def init_app(self: Self) -> None:
        engine.gfx.viewport(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        engine.gfx.clear_color(0.2, 0.2, 0.2)
        engine.gfx.enable(gl.GL_DEPTH_TEST)
        return super().init_app()

    def init_frame(self: Self) -> None:
        return super().init_frame()
