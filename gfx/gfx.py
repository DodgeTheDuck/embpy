from enum import Enum
import OpenGL.GL as gl
import glm
import core.engine as engine

from typing import Self
from pyparsing import deque
from core.node_graph import Node, NodeGraph
from gfx.material import Material
from gfx.mesh_node import MeshNode
from gfx.pipeline.pipeline import Pipeline
from gfx.pipeline.pipeline_stage import PipelineStage
from gfx.renderer_setup.renderer_setup import RendererSetup
from gfx.shader_program import ShaderProgram


class GlConstants(Enum):
    gl_lequal = gl.GL_LEQUAL
    gl_less = gl.GL_LESS


class Gfx:
    def __init__(self: Self, renderer_setup: RendererSetup) -> None:

        self.renderer_setup = renderer_setup

        self.model_stack = deque[glm.mat4]()
        self.view_stack = deque[glm.mat4]()
        self.proj_stack = deque[glm.mat4]()

        self.pipeline = Pipeline()
        self.active_pipeline_stage: PipelineStage = None
        self.active_shader_program: ShaderProgram = None

    def init_gl(self: Self) -> None:
        self.renderer_setup.init_app()

    def apply_mvp(self: Self) -> None:
        m = self.model_stack[-1]
        v = self.view_stack[-1]
        p = self.proj_stack[-1]

        if "m" in self.active_shader_program.uniforms:
            self.uni_mat4(self.get_active_shader_program(), "m", m)
        if "v" in self.active_shader_program.uniforms:
            self.uni_mat4(self.get_active_shader_program(), "v", v)
        if "p" in self.active_shader_program.uniforms:
            self.uni_mat4(self.get_active_shader_program(), "p", p)

    def push_mat_model(self: Self, mat: glm.mat4) -> None:
        if len(self.model_stack) == 0:
            self.model_stack.append(mat)
        else:
            self.model_stack.append(self.model_stack[-1] * mat)

    def push_mat_view(self: Self, mat: glm.mat4) -> None:
        if len(self.model_stack) == 0:
            self.view_stack.append(mat)
        else:
            self.view_stack.append(self.view_stack[-1] * mat)

    def push_mat_proj(self: Self, mat: glm.mat4) -> None:
        if len(self.model_stack) == 0:
            self.proj_stack.append(mat)
        else:
            self.proj_stack.append(self.proj_stack[-1] * mat)

    def pop_mat_model(self: Self) -> None:
        self.model_stack.pop()

    def pop_mat_view(self: Self) -> None:
        self.view_stack.pop()

    def pop_mat_proj(self: Self) -> None:
        self.proj_stack.pop()

    def get_active_pipeline(self: Self) -> Pipeline:
        return self.pipeline

    def get_active_shader_program(self: Self) -> ShaderProgram:
        return self.active_shader_program

    def set_pipeline(self: Self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline

    def draw_mesh_tree(self: Self, mesh_tree_root: NodeGraph[MeshNode], material: Material) -> None:
        self.__draw_mesh_node(mesh_tree_root, material)

    def __draw_mesh_node(self: Self, node: Node[MeshNode], material: Material) -> None:
        if node.obj is not None:
            self.push_mat_model(node.obj.transform.as_mat4())
            for mesh in node.obj.meshes:
                mesh.bind()
                self.apply_mvp()
                material.apply_properties(mesh.material_properties)
                if mesh.do_lighting:
                    engine.scene.light_manager.apply_lights()
                gl.glDrawElements(gl.GL_TRIANGLES,
                                  mesh.n_indices,
                                  mesh.index_type,
                                  None)
        else:
            self.push_mat_model(glm.mat4())
        for child in node.children:
            self.__draw_mesh_node(child, material)

        self.pop_mat_model()

# region Wrapper Functions

    def use_shader_program(self: Self, shader_program: ShaderProgram) -> None:
        self.active_shader_program = shader_program
        gl.glUseProgram(shader_program.program)

    def depth_function(self: Self, gl_depth_func: GlConstants) -> None:
        gl.glDepthFunc(gl_depth_func.value)

    def enable(self: Self, gl_enable_hint: int) -> None:
        gl.glEnable(gl_enable_hint)

    def viewport(self: Self, x: float, y: float, width: float, height: float) -> None:
        gl.glViewport(x, y, width, height)

    def clear_color(self: Self, r: float, g: float, b: float) -> None:
        gl.glClearColor(r, g, b, 1.0)

    def clear(self: Self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def uni_mat4(self: Self, shader: ShaderProgram, name: str, mat: glm.mat4) -> None:
        gl.glUniformMatrix4fv(shader.get_uniform_loc(name),
                              1,
                              gl.GL_FALSE,
                              glm.value_ptr(mat))

    def uni_vec3(self: Self, shader: ShaderProgram, name: str, vec: glm.vec3) -> None:
        gl.glUniform3f(shader.get_uniform_loc(name), vec.x, vec.y, vec.z)

    def uni_float1(self: Self, shader: ShaderProgram, name: str, fl: float) -> None:
        gl.glUniform1f(shader.get_uniform_loc(name), fl)

    def uni_int1(self: Self, shader: ShaderProgram, name: str, i: int) -> None:
        gl.glUniform1i(shader.get_uniform_loc(name), i)

# endregion
