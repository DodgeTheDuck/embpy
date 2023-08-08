
from enum import Enum
from typing import Self
import OpenGL.GL as gl
import config


class FBO:
    def __init__(self: Self) -> None:
        self.buffer = gl.glGenFramebuffers(1)
        self.textures = list[int]()
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.buffer)

        tex_position = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_position)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB16F, config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 0, gl.GL_RGB, gl.GL_FLOAT, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, tex_position, 0)

        tex_normal = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_normal)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB16F, config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 0, gl.GL_RGB, gl.GL_FLOAT, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT1, gl.GL_TEXTURE_2D, tex_normal, 0)

        tex_albedo = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_albedo)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT2, gl.GL_TEXTURE_2D, tex_albedo, 0)

        tex_met_rough = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex_met_rough)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT3, gl.GL_TEXTURE_2D, tex_met_rough, 0)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glDrawBuffers([gl.GL_COLOR_ATTACHMENT0, gl.GL_COLOR_ATTACHMENT1, gl.GL_COLOR_ATTACHMENT2, gl.GL_COLOR_ATTACHMENT3])

        self.textures.append(tex_position)
        self.textures.append(tex_normal)
        self.textures.append(tex_albedo)
        self.textures.append(tex_met_rough)

        rbo = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_STENCIL_ATTACHMENT, gl.GL_RENDERBUFFER, rbo)

        if not gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("framebuffer failed")

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
