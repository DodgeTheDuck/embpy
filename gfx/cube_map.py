
import io
from typing import Self
import OpenGL.GL as gl
from PIL import Image
import numpy


class CubeMap:
    def __init__(self: Self, faces: str[6]) -> None:

        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture)

        for index, face_path in enumerate(faces):
            image = Image.open(io.BytesIO(face_path))
            if image.mode == "P":  # (palettised) : convert this to RGBA
                image = image.convert()
            image_data = numpy.array(list(image.getdata()), numpy.uint8)
            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + index,
                            0,
                            gl.GL_RGB,
                            image.width,
                            image.height,
                            0, gl.GL_RGB,
                            gl.GL_UNSIGNED_BYTE,
                            image_data)

        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_TEXTURE_WRAP_S)
        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_TEXTURE_WRAP_T)
        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_TEXTURE_WRAP_R)
        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_CLAMP_TO_EDGE)
        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_CLAMP_TO_EDGE)
        self.__tex_param(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_CLAMP_TO_EDGE)

        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)

    def __tex_param(self: Self, target: int, name: int, param: int) -> None:
        if param == 0: return
        gl.glTexParameteri(target,
                           name,
                           param)
