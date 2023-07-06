
from ctypes import c_float
from typing import Self
import OpenGL.GL as gl


class VBO:
    def __init__(self: Self,
                 data: list[float]) -> None:

        self.buffer = gl.glGenBuffers(1)
        self.n_verts = len(data)

        # position buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        (c_float*len(data))(*data),
                        gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def setup_attributes(self: Self, location: int, size: int) -> None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glEnableVertexAttribArray(location)
        gl.glVertexAttribPointer(location,
                                 size,
                                 gl.GL_FLOAT,
                                 gl.GL_FLOAT,
                                 0,
                                 None)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
