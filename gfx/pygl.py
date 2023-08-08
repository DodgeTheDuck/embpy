from typing import Self
import OpenGL.GL as gl
import glm
from pyparsing import deque
from gfx.pipeline import Pipeline
from gfx.pipeline_stage import PipelineStage

from gfx.shader_program import ShaderProgram
from gfx.texture import Sampler, Texture
from loaders.shader_loader import ShaderLoader


class Pygl:
    def __init__(self: Self) -> None:
        self.shaders = dict[str, ShaderProgram]()
        self.model_stack = deque[glm.mat4]()
        self.view_stack = deque[glm.mat4]()
        self.proj_stack = deque[glm.mat4]()

        self.pipeline_stage = deque[PipelineStage]()

        self.model_mat_acc = glm.mat4(1.0)
        self.model_view_acc = glm.mat4(1.0)
        self.mode_proj_acc = glm.mat4(1.0)

        self.pipeline = Pipeline()

        geometry_loader = ShaderLoader("assets/shader/geometry.shader")
        geometry_shader = geometry_loader.load()

        light_pass_loader = ShaderLoader("assets/shader/light_pass.shader")
        light_pass_shader = light_pass_loader.load()

        shading_loader = ShaderLoader("assets/shader/pbr_shader.shader")
        shading_shader = shading_loader.load()

        composite_loader = ShaderLoader("assets/shader/fbo_draw.shader")
        composite_shader = composite_loader.load()

        self.pipeline.add_stage("geometry", PipelineStage("geometry", geometry_shader, composite_shader))
        self.pipeline.add_stage("light_pass", PipelineStage("light_pass", light_pass_shader, composite_shader))
        self.pipeline.add_stage("shading", PipelineStage("shading", shading_shader, composite_shader))

        empty_tex_sampler = Sampler()
        empty_tex_sampler.tex_min_filter = gl.GL_NEAREST
        empty_tex_sampler.tex_mag_filter = gl.GL_NEAREST
        empty_tex_sampler.tex_wrap_s = gl.GL_REPEAT
        empty_tex_sampler.tex_wrap_t = gl.GL_REPEAT
        empty_tex_sampler.target = gl.GL_TEXTURE_2D
        self.empty_texture = Texture("./textures/empty_tex.bmp", empty_tex_sampler)

    def init_gl(self: Self, window_width: int, window_height: int) -> None:
        gl.glViewport(0, 0, window_width, window_height)
        # gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def clear_color(self: Self, r: float, g: float, b: float) -> None:
        gl.glClearColor(r, g, b, 1.0)

    def clear(self: Self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # def add_shader(self: Self,
    #                prog_name: str,
    #                frag_name: str,
    #                vert_name: str) -> int:
    #     frag_shader = Shader(ShaderType.fragment, frag_name)
    #     vert_shader = Shader(ShaderType.vertex, vert_name)
    #     frag_shader.compile()
    #     vert_shader.compile()
    #     shader_program = ShaderProgram([frag_shader, vert_shader])
    #     shader_program.compile()
    #     self.shaders[prog_name] = shader_program
    #     return shader_program.program

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

    def bind_empty_texture(self: Self) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D,
                         self.empty_texture.texture)

    def push_pipeline_stage(self: Self, name: str) -> PipelineStage:
        stage = self.pipeline.stages[name]
        stage.bind()
        self.pipeline_stage.append(stage)
        return stage

    def pop_pipeline_stage(self: Self) -> None:
        self.pipeline_stage.pop()

    def top_pipeline_stage(self: Self) -> PipelineStage:
        return self.pipeline_stage[-1]

    def bind_default_framebuffer(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
