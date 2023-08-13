
from typing import Self
import OpenGL.GL as gl


class VAO:
    def __init__(self: Self) -> None:
        self.buffer = gl.glGenVertexArrays(1)

    def bind(self: Self) -> None:
        gl.glBindVertexArray(self.buffer)

    def unbind(self: Self) -> None:
        gl.glBindVertexArray(0)
