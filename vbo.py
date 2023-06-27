
from ctypes import c_float
import functools
import operator
from typing import Self
import OpenGL.GL as gl

from geometry import Vertex


class VBO:
    def __init__(self: Self, verts: list[Vertex]) -> None:
        self.buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        arr: list[float] = functools.reduce(operator.iconcat,
                                            [v.pack() for v in verts],
                                            [])
        self.n_verts = len(verts)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        len(arr) * 4,
                        (c_float*len(arr))(*arr),
                        gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FLOAT, 0, None)

    def draw(self: Self) -> None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.n_verts)
