
import array
from ctypes import c_uint
from typing import Self
import OpenGL.GL as gl


class IBO:
    def __init__(self: Self, indices: array.array) -> None:
        self.buffer = gl.glGenBuffers(1)
        self.indices = indices
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.buffer)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
                        (c_uint * len(indices))(*indices),
                        gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        pass
