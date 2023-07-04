
from ctypes import c_float
from typing import Self
import OpenGL.GL as gl


class VBO:
    def __init__(self: Self, data: list[float], size: int, location: int) -> None:

        self.buffer = gl.glGenBuffers(1)
        self.n_verts = len(data)

        # position buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        (c_float*len(data))(*data),
                        gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(location)
        gl.glVertexAttribPointer(location,
                                 size,
                                 gl.GL_FLOAT,
                                 gl.GL_FLOAT,
                                 0,
                                 None)
