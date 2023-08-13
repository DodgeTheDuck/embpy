
from typing import Self
import OpenGL.GL as gl

from gfx.attachment import Attachment


class FBO:
    def __init__(self: Self) -> None:
        self.buffer = gl.glGenFramebuffers(1)
        self.attachments = list[Attachment]()

    def bind(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.buffer)

    def add_attachment(self: Self, index: int, att: Attachment) -> None:
        self.bind()
        tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, att.internal_format, att.width, att.height, 0, att.format, att.gl_type, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, att.attachment_location(index), gl.GL_TEXTURE_2D, tex, 0)
        att.texture = tex
        self.attachments.append(att)
        pass
