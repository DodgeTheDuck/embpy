from typing import Self
import OpenGL.GL as gl


class Pygl:
    def __init__(self: Self) -> None:
        pass

    def init_gl(self: Self, window_width: int, window_height: int) -> None:
        gl.glViewport(0, 0, window_width, window_height)
        gl.glClearColor(0.2, 0.5, 0.5, 1.0)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

    def clear(self: Self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
