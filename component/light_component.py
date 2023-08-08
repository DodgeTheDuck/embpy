
from typing import Self

from component.component import Component
from component.transform_component import TransformComponent
from core.node_graph import Node, NodeGraph
from gfx.mesh import Mesh
from gfx.mesh_node import MeshNode
from gfx.shader_program import ShaderProgram
from scene.scene_object import SceneObject
import OpenGL.GL as gl
import core.pg as pg


class LightComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.volume = NodeGraph[list[Mesh]]()
        super().__init__(owner, "Light")

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
            scene_shader = pg.gl().top_pipeline_stage().draw_shader
            pg.gl().push_mat_model(transform.transform.as_mat4())
            self._draw_node(self.volume.root, scene_shader)
            pg.gl().pop_mat_model()

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
