
from typing import Self
import OpenGL.GL as gl

from gfx.attachment import Attachment, AttachmentType


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
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
        if att.att_type == AttachmentType.DEPTH:
            gl.glTexParameterfv(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BORDER_COLOR, (1.0, 1.0, 1.0, 1.0))
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_COMPARE_MODE, gl.GL_COMPARE_REF_TO_TEXTURE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_COMPARE_FUNC, gl.GL_LEQUAL)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, att.internal_format, att.width, att.height, 0, att.format, att.gl_type, None)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, att.attachment_location(index), gl.GL_TEXTURE_2D, tex, 0)

        status = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
        if status != gl.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("incomplete framebuffer")

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        att.texture = tex
        self.attachments.append(att)
        pass
