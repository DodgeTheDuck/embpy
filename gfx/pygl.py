from typing import Self
import OpenGL.GL as gl
import glm
from pyparsing import deque
from gfx.pipeline.pipeline import Pipeline
from gfx.pipeline.pipeline_stage import PipelineStage
from gfx.renderer_setup.renderer_setup import RendererSetup
from gfx.shader_program import ShaderProgram


class Pygl:
    def __init__(self: Self, renderer_setup: RendererSetup) -> None:

        self.renderer_setup = renderer_setup

        self.model_stack = deque[glm.mat4]()
        self.view_stack = deque[glm.mat4]()
        self.proj_stack = deque[glm.mat4]()

        self.pipeline = Pipeline()
        self.active_pipeline_stage: PipelineStage = None

    def init_gl(self: Self) -> None:
        self.renderer_setup.init_app()

    def apply_mvp(self: Self, program: int) -> None:
        m = self.model_stack[-1]
        v = self.view_stack[-1]
        p = self.proj_stack[-1]
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
        if len(self.model_stack) == 0:
            self.view_stack.append(mat)
        else:
            self.view_stack.append(mat * self.view_stack[-1])

    def push_mat_proj(self: Self, mat: glm.mat4) -> None:
        if len(self.model_stack) == 0:
            self.proj_stack.append(mat)
        else:
            self.proj_stack.append(mat * self.proj_stack[-1])

    def pop_mat_model(self: Self) -> None:
        self.model_stack.pop()

    def pop_mat_view(self: Self) -> None:
        self.view_stack.pop()

    def pop_mat_proj(self: Self) -> None:
        self.proj_stack.pop()

    def get_active_pipeline(self: Self) -> Pipeline:
        return self.pipeline

    def set_pipeline(self: Self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline

    # GL WRAPPER

    def enable(self: Self, gl_enable_hint: int) -> None:
        gl.glEnable(gl_enable_hint)

    def viewport(self: Self, x: float, y: float, width: float, height: float) -> None:
        gl.glViewport(x, y, width, height)

    def clear_color(self: Self, r: float, g: float, b: float) -> None:
        gl.glClearColor(r, g, b, 1.0)

    def clear(self: Self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def use_program(self: Self, program: int) -> None:
        gl.glUseProgram(program)

    def uni_mat4(self: Self, program: int, name: str, mat: glm.mat4) -> None:
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(program, name),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mat))

    def uni_vec3(self: Self, shader: ShaderProgram, name: str, vec: glm.vec3) -> None:
        # TODO: add support for structs/arrays in shader compiler
        gl.glUniform3f(gl.glGetUniformLocation(shader.program, name), vec.x, vec.y, vec.z)

    def uni_float1(self: Self, shader: ShaderProgram, name: str, fl: float) -> None:
        gl.glUniform1f(gl.glGetUniformLocation(shader.program, name), fl)
