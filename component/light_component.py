
from enum import Enum
from typing import Self

from glm import vec3

from component.component import Component
from component.transform_component import TransformComponent
from core.node_graph import Node, NodeGraph
from gfx.mesh import Mesh
from gfx.mesh_node import MeshNode
from gfx.shader_program import ShaderProgram
from scene.scene_object import SceneObject
import OpenGL.GL as gl
import core.pg as pg


class LightType(Enum):
    none = 0
    point = 1
    directional = 2


class LightComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.volume = NodeGraph[list[Mesh]]()
        self.color = vec3(1, 1, 1)
        self.intensity = 1
        self.type = LightType.none
        self.direction = vec3(0, 0, 0)
        super().__init__(owner, "Light")

    def set_color(self: Self, color: vec3) -> Self:
        self.color = color
        return self

    def set_intensity(self: Self, intensity: float) -> Self:
        self.intensity = intensity
        return self

    def set_type(self: Self, type: LightType) -> Self:
        self.type = type
        return self

    def set_direction(self: Self, direction: vec3) -> Self:
        self.direction = direction
        return self

    def set_volume_mesh(self: Self, mesh_tree: NodeGraph[list[Mesh]]) -> Self:
        self.volume = mesh_tree
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw_pass_geometry(self: Self) -> None:
        return super().draw_pass_geometry()

    def draw_pass_lighting(self: Self) -> None:
        transform = self.owner.get_component(TransformComponent)
        if transform is not None:
            gl.glCullFace(gl.GL_FRONT)
            scene_shader = pg.gl().get_active_pipeline_stage().draw_shader
            gl.glUniform3f(scene_shader.get_uniform_loc("LightPos"), transform.transform.position.x, transform.transform.position.y, transform.transform.position.z)
            gl.glUniform3f(scene_shader.get_uniform_loc("LightColor"), self.color.x, self.color.y, self.color.z)
            gl.glUniform3f(scene_shader.get_uniform_loc("LightDir"), self.direction.x, self.direction.y, self.direction.z)
            gl.glUniform1f(scene_shader.get_uniform_loc("LightIntensity"), self.intensity)
            gl.glUniform1i(scene_shader.get_uniform_loc("LightType"), self.type.value)
            pg.gl().push_mat_model(transform.transform.as_mat4())
            self._draw_node(self.volume.root, scene_shader)
            pg.gl().pop_mat_model()
            gl.glCullFace(gl.GL_BACK)

        return super().draw_pass_lighting()

    def _draw_node(self: Self, node: Node[MeshNode], scene_shader: ShaderProgram) -> None:

        pg.gl().push_mat_model(node.obj.transform.as_mat4())

        program = scene_shader.program

        for mesh in node.obj.meshes:
            pg.gl().apply_mvp(program)
            mesh.vao.bind()

            gl.glDrawElements(gl.GL_TRIANGLES,
                              mesh.n_indices,
                              mesh.index_type,
                              None)

            mesh.vao.unbind()

        for child in node.children:
            self._draw_node(child, scene_shader)

        pg.gl().pop_mat_model()
