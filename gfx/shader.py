
from enum import Enum
from typing import Self
import OpenGL.GL as gl


class ShaderType(Enum):
    none = 0
    fragment = 1
    vertex = 2


class Shader:
    def __init__(self: Self, type: ShaderType, src: str, uniforms: list[str]) -> None:
        self.type: ShaderType = type
        self.uniforms = uniforms
        self.src = src
        self.shader = None

    def compile(self: Self) -> None:
        match self.type:
            case ShaderType.fragment:
                self.shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
            case ShaderType.vertex:
                self.shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.shader, self.src)
        gl.glCompileShader(self.shader)
        err = gl.glGetShaderiv(self.shader, gl.GL_COMPILE_STATUS)
        if err != gl.GL_TRUE:
            info = gl.glGetShaderInfoLog(self.shader)
            raise Exception(info)
