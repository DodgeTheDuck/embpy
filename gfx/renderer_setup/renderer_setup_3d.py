
from typing import Self
from gfx.renderer_setup.renderer_setup import RendererSetup
import core.pg as pg
import OpenGL.GL as gl
import config


class RendererSetup3d(RendererSetup):
    def __init__(self: Self) -> None:
        super().__init__()

    def init_app(self: Self) -> None:
        pg.gl().viewport(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        pg.gl().enable(gl.GL_DEPTH_TEST)
        return super().init_app()

    def init_frame(self: Self) -> None:
        return super().init_frame()
