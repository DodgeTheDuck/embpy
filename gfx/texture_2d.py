
import io
from typing import Self
import OpenGL.GL as gl
from PIL import Image
import numpy

from gfx.texture import Texture

# TODO:
# - handle image format better
# - make class better


class Sampler:
    def __init__(self: Self) -> None:
        self.target: int = 0
        self.tex_wrap_s: int = 0
        self.tex_wrap_t: int = 0
        self.tex_wrap_r: int = 0
        self.tex_min_filter: int = 0
        self.tex_mag_filter: int = 0
        self.n_faces: int = 0
        pass


class Texture2D(Texture):
    def __init__(self: Self, data: str | bytes, sampler: Sampler) -> None:
        super().__init__()

        image: Image = None

        if isinstance(data, str):
            image = Image.open(data)
        elif isinstance(data, bytes):
            image = Image.open(io.BytesIO(data))
        else:
            raise Exception("Invalid data param")

        if image.mode == "P":  # (palettised) : convert this to RGBA
            image = image.convert()

        image_data = numpy.array(list(image.getdata()), numpy.uint8)

        self.sampler = sampler
        self.texture = gl.glGenTextures(1)

        gl.glBindTexture(sampler.target, self.texture)

        self.__tex_param(sampler.target, gl.GL_TEXTURE_WRAP_S, sampler.tex_wrap_s)
        self.__tex_param(sampler.target, gl.GL_TEXTURE_WRAP_T, sampler.tex_wrap_t)
        self.__tex_param(sampler.target, gl.GL_TEXTURE_WRAP_R, sampler.tex_wrap_r)
        self.__tex_param(sampler.target, gl.GL_TEXTURE_MIN_FILTER, sampler.tex_min_filter)
        self.__tex_param(sampler.target, gl.GL_TEXTURE_MAG_FILTER, sampler.tex_mag_filter)

        internal_format = 0
        format = 1

        if image.mode == "RGBA":
            internal_format = gl.GL_RGBA
            format = gl.GL_RGBA
        elif image.mode == "RGB":
            internal_format = gl.GL_RGB
            format = gl.GL_RGB
        elif image.mode == "1":
            internal_format = gl.GL_RED
            format = gl.GL_RED
        else:
            raise Exception(f"invalid texture format: {image.mode}")

        gl.glTexImage2D(sampler.target,
                        0,
                        internal_format,
                        image.width,
                        image.height,
                        0,
                        format,
                        gl.GL_UNSIGNED_BYTE,
                        image_data)

        gl.glGenerateMipmap(sampler.target)
        gl.glBindTexture(sampler.target, 0)

    def bind(self: Self, index: int) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0 + index)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

    def __tex_param(self: Self, target: int, name: int, param: int) -> None:
        if param == 0: return
        gl.glTexParameteri(target,
                           name,
                           param)
