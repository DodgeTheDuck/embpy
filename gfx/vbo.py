
from typing import Self
import OpenGL.GL as gl


class VBO:
    def __init__(self: Self,
                 data: bytes,
                 target: int) -> None:

        self.buffer = gl.glGenBuffers(1)
        self.target = target

        gl.glBindBuffer(target, self.buffer)
        gl.glBufferData(target,
                        data,
                        gl.GL_STATIC_DRAW)
        gl.glBindBuffer(target, 0)

    def bind(self: Self) -> None:
        gl.glBindBuffer(self.target, self.buffer)

    def unbind(self: Self) -> None:
        gl.glBindBuffer(self.target, 0)
