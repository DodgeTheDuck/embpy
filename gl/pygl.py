from typing import Self
import OpenGL.GL as gl
import glm
from pyparsing import deque

from gl.shader import Shader, ShaderType
from gl.shader_program import ShaderProgram


class Pygl:
    def __init__(self: Self) -> None:
        self.shaders = dict[str, ShaderProgram]()
        self.model_stack = deque[glm.mat4]()
        self.view_stack = deque[glm.mat4]()
        self.proj_stack = deque[glm.mat4]()

    def init_gl(self: Self, window_width: int, window_height: int) -> None:
        gl.glViewport(0, 0, window_width, window_height)
        gl.glClearColor(0.2, 0.5, 0.5, 1.0)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)

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

    def get_program(self: Self, prog_name: str) -> int:
        return self.shaders[prog_name].program

    def use_program(self: Self, program: int) -> None:
        gl.glUseProgram(program)

    def uni_mat4(self: Self, program: int, var: str, mat: glm.mat4) -> None:
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, var),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mat))

    def apply_mvp(self: Self, program: int) -> None:
        m = self.model_stack[-1]
        v = self.view_stack[-1]
        p = self.proj_stack[-1]
        mvp = p * v * m
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, "mvp"),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mvp))

    def push_mat_model(self: Self, mat: glm.mat4) -> None:
        self.model_stack.append(mat)

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
