
import ctypes
from typing import Self
import OpenGL.GL as gl


class Attribute:
    def __init__(self: Self, location: int, size: int, type: int, offset: int, stride: int) -> None:
        self.location = location
        self.size = size
        self.type = type
        self.stride = stride
        self.offset = offset

    def bind(self: Self) -> None:
        gl.glEnableVertexAttribArray(self.location)
        gl.glVertexAttribPointer(self.location,
                                 self.size,
                                 self.type,
                                 gl.GL_FALSE,
                                 self.stride or 0,
                                 ctypes.c_void_p(self.offset))
