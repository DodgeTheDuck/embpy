
import ctypes
from enum import Enum
from typing import Self
import OpenGL.GL as gl


class AttributeType(Enum):
    NONE = 0
    POSITION = 1
    NORMAL = 2
    TANGENT = 3
    TEX_COORD = 4


class Attribute:
    def __init__(self: Self, att_type: AttributeType, location: int, size: int, type: int, offset: int, stride: int) -> None:
        self.att_type = att_type
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
