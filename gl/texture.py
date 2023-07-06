
from typing import Self
import OpenGL.GL as gl
from PIL import Image
import numpy

# TODO:
# - don't like random numpy usage. find better way to do this
# - handle image format better


class Texture:
    def __init__(self: Self, filename: str) -> None:

        image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
        image_data = numpy.array(list(image.getdata()), numpy.uint8)

        self.texture = gl.glGenTextures(1)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_WRAP_S,
                           gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_WRAP_T,
                           gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_NEAREST)

        if image.mode == "RGBA":
            gl.glTexImage2D(gl.GL_TEXTURE_2D,
                            0,
                            gl.GL_RGBA,
                            image.width,
                            image.height,
                            0,
                            gl.GL_RGBA,
                            gl.GL_UNSIGNED_BYTE,
                            image_data)
        elif image.mode == "RGB":
            gl.glTexImage2D(gl.GL_TEXTURE_2D,
                            0,
                            gl.GL_RGB,
                            image.width,
                            image.height,
                            0,
                            gl.GL_RGB,
                            gl.GL_UNSIGNED_BYTE,
                            image_data)
        else:
            raise Exception(f"invalid texture format: {image.mode}")

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
