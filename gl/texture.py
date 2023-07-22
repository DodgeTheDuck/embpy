
from typing import Self
import OpenGL.GL as gl
from PIL import Image
import numpy

# TODO:
# - handle image format better
# - make class better


class Sampler:
    def __init__(self: Self) -> None:
        self.target: int = 0
        self.tex_wrap_s: int = 0
        self.tex_wrap_t: int = 0
        self.tex_min_filter: int = 0
        self.tex_mag_filter: int = 0
        pass


class Texture:
    def __init__(self: Self, filename: str, sampler: Sampler) -> None:

        image = Image.open(filename)

        if image.mode == "P":  # (palettised) : convert this to RGBA
            image = image.convert()

        image_data = numpy.array(list(image.getdata()), numpy.uint8)

        self.sampler = sampler
        self.texture = gl.glGenTextures(1)
        # gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glBindTexture(sampler.target, self.texture)
        gl.glTexParameteri(sampler.target,
                           gl.GL_TEXTURE_WRAP_S,
                           sampler.tex_wrap_s)
        gl.glTexParameteri(sampler.target,
                           gl.GL_TEXTURE_WRAP_T,
                           sampler.tex_wrap_t)
        gl.glTexParameteri(sampler.target,
                           gl.GL_TEXTURE_MIN_FILTER,
                           sampler.tex_min_filter)
        gl.glTexParameteri(sampler.target,
                           gl.GL_TEXTURE_MAG_FILTER,
                           sampler.tex_mag_filter)

        if image.mode == "RGBA":
            gl.glTexImage2D(sampler.target,
                            0,
                            gl.GL_RGBA,
                            image.width,
                            image.height,
                            0,
                            gl.GL_RGBA,
                            gl.GL_UNSIGNED_BYTE,
                            image_data)
            gl.glGenerateMipmap(sampler.target)
        elif image.mode == "RGB":
            gl.glTexImage2D(sampler.target,
                            0,
                            gl.GL_RGB,
                            image.width,
                            image.height,
                            0,
                            gl.GL_RGB,
                            gl.GL_UNSIGNED_BYTE,
                            image_data)
            gl.glGenerateMipmap(sampler.target)
        else:
            raise Exception(f"invalid texture format: {image.mode}")

        gl.glBindTexture(sampler.target, 0)
