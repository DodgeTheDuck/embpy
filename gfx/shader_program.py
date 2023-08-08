from typing import Any, Self

import glm
import OpenGL.GL as gl

from gfx.shader import Shader


class ShaderProgram:
    def __init__(self: Self, shaders: list[Shader]) -> None:
        self.program = None
        self.shaders = shaders
        self.uni_mvp = None
        self.uniforms = dict[str, int]()

    def compile(self: Self) -> None:
        self.program = gl.glCreateProgram()
        for shader in self.shaders:
            gl.glAttachShader(self.program, shader.shader)
        gl.glLinkProgram(self.program)
        err: Any = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if err != gl.GL_TRUE:
            info = gl.glGetShaderInfoLog(self.program)
            raise Exception(info)

        for shader in self.shaders:
            for uniform in shader.uniforms:
                self.uniforms[uniform] = gl.glGetUniformLocation(self.program, uniform)

    def get_uniform_loc(self: Self, name: str) -> int:
        return self.uniforms[name]

    def set_mvp(self: Self, mvp: glm.mat4) -> None:
        gl.glUniformMatrix4fv(self.uni_mvp,
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mvp))

    def use(self: Self) -> None:
        gl.glUseProgram(self.program)
