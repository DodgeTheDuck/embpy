from typing import Self
import OpenGL.GL as gl
import glm
from pyparsing import deque

from gl.shader import Shader, ShaderType
from gl.shader_program import ShaderProgram
from gl.texture import Sampler, Texture


class Pygl:
    def __init__(self: Self) -> None:
        self.shaders = dict[str, ShaderProgram]()
        self.model_stack = deque[glm.mat4]()
        self.view_stack = deque[glm.mat4]()
        self.proj_stack = deque[glm.mat4]()

        self.model_mat_acc = glm.mat4(1.0)
        self.model_view_acc = glm.mat4(1.0)
        self.mode_proj_acc = glm.mat4(1.0)

        empty_tex_sampler = Sampler()
        empty_tex_sampler.tex_min_filter = gl.GL_NEAREST
        empty_tex_sampler.tex_mag_filter = gl.GL_NEAREST
        empty_tex_sampler.tex_wrap_s = gl.GL_REPEAT
        empty_tex_sampler.tex_wrap_t = gl.GL_REPEAT
        empty_tex_sampler.target = gl.GL_TEXTURE_2D
        self.empty_texture = Texture("./textures/empty_tex.bmp", empty_tex_sampler)

    def init_gl(self: Self, window_width: int, window_height: int) -> None:
        gl.glViewport(0, 0, window_width, window_height)
        gl.glClearColor(0.2, 0.5, 0.5, 1.0)
        # gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def clear(self: Self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def add_shader(self: Self,
                   prog_name: str,
                   frag_name: str,
                   vert_name: str) -> int:
        frag_shader = Shader(ShaderType.fragment, frag_name)
        vert_shader = Shader(ShaderType.vertex, vert_name)
        frag_shader.compile()
        vert_shader.compile()
        shader_program = ShaderProgram([frag_shader, vert_shader])
        shader_program.compile()
        self.shaders[prog_name] = shader_program
        return shader_program.program

    def get_shader(self: Self, prog_name: str) -> ShaderProgram:
        return self.shaders[prog_name]

    def get_program(self: Self, prog_name: str) -> int:
        return self.shaders[prog_name].program

    def use_program(self: Self, program: int) -> None:
        gl.glUseProgram(program)

    def uni_mat4(self: Self, program: int, var: str, mat: glm.mat4) -> None:
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, var),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mat))

    def mult_mat_stack(self: Self, mat_stack: deque[glm.mat4]) -> glm.mat4:
        result: glm.mat4 = None
        for mat in mat_stack:
            if result is None:
                result = mat
            else:
                result *= mat
        return result

    def apply_mvp(self: Self, program: int) -> None:
        m = self.mult_mat_stack(self.model_stack)
        v = self.mult_mat_stack(self.view_stack)
        p = self.mult_mat_stack(self.proj_stack)
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, "m"),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(m))
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, "v"),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(v))
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, "p"),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(p))

    def push_mat_model(self: Self, mat: glm.mat4) -> None:
        if len(self.model_stack) == 0:
            self.model_stack.append(mat)
        else:
            self.model_stack.append(mat * self.model_stack[-1])

    def push_mat_view(self: Self, mat: glm.mat4) -> None:
        self.view_stack.append(mat)

    def push_mat_proj(self: Self, mat: glm.mat4) -> None:
        self.proj_stack.append(mat)

    def pop_mat_model(self: Self) -> None:
        self.model_stack.pop()

    def pop_mat_view(self: Self) -> None:
        self.view_stack.pop()

    def pop_mat_proj(self: Self) -> None:
        self.proj_stack.pop()

    def bind_empty_texture(self: Self) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D,
                         self.empty_texture.texture)
