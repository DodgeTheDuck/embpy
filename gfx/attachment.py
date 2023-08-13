
from enum import Enum
from typing import Self
import OpenGL.GL as gl

class AttachmentType(Enum):
    NONE = 0
    COLOR = 1
    DEPTH = 2


class Attachment:
    def __init__(self: Self, name: str, att_type: AttachmentType, width: int, height: int, internal_format: int, format: int, gl_type: int) -> None:
        self.name = name
        self.att_type = att_type
        self.width = width
        self.height = height
        self.internal_format = internal_format
        self.format = format
        self.gl_type = gl_type
        self.texture = None

    def attachment_location(self: Self, index: int) -> int:
        if self.att_type == AttachmentType.COLOR:
            return gl.GL_COLOR_ATTACHMENT0 + index
        if self.att_type == AttachmentType.DEPTH:
            return gl.GL_DEPTH_ATTACHMENT

    def set_texture(self: Self, texture_handle: int) -> None:
        self.texture = texture_handle
