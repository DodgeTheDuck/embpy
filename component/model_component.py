from component.transform_component import TransformComponent
from material import Material, TextureType
from mesh_node import MeshNode
from node_graph import Node, NodeGraph
import pg
from typing import Self
from component.component import Component
from mesh import Mesh
from scene.scene_object import SceneObject
import OpenGL.GL as gl
import imgui

# TODO:
# - handle material stuff better


class ModelComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.mesh_tree: NodeGraph[list[Mesh]] = None
        super().__init__(owner, "Model")
        pass

    def set_mesh_tree(self: Self, mesh_tree: NodeGraph[list[Mesh]]) -> Self:
        self.mesh_tree = mesh_tree
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw(self: Self) -> None:
        transform = self.owner.get_component(TransformComponent)
        if transform is not None:
            scene = pg.gl().get_shader("scene")
            pg.gl().push_mat_model(transform.transform.as_mat4())

            gl.glUniform1i(scene.uni_tex_albedo, 0)
            gl.glUniform1i(scene.uni_tex_met_rough, 1)

            self._draw_node(self.mesh_tree.root, scene.program)

            pg.gl().pop_mat_model()

        return super().draw()

    def _draw_node(self: Self, node: Node[MeshNode], program: int) -> None:

        pg.gl().push_mat_model(node.obj.transform.as_mat4())

        for mesh in node.obj.meshes:
            material: Material = mesh.material
            pg.gl().apply_mvp(program)
            mesh.vao.bind()
            gl.glUniform1i(gl.glGetUniformLocation(program, "hasTexture"), 1)

            if material.has_texture(TextureType.albedo):
                texture = material.get_texture(TextureType.albedo).texture
                gl.glActiveTexture(gl.GL_TEXTURE0)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            if material.has_texture(TextureType.metallic_roughness):
                texture = material.get_texture(TextureType.metallic_roughness).texture
                gl.glActiveTexture(gl.GL_TEXTURE1)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            # else:
            #     gl.glUniform1i(gl.glGetUniformLocation(program,
            #                                            "hasTexture"), 0)
            #     pg.gl().bind_empty_texture()

            gl.glDrawElements(gl.GL_TRIANGLES,
                              mesh.n_indices,
                              mesh.index_type,
                              None)

            mesh.vao.unbind()

        for child in node.children:
            self._draw_node(child, program)

        pg.gl().pop_mat_model()

    def gui(self: Self) -> None:
        self._draw_node_gui(self.mesh_tree.root)
        return super().gui()

    def _draw_node_gui(self: Self, node: Node[MeshNode]) -> None:
        if imgui.tree_node(node.obj.name, flags=imgui.TREE_NODE_DEFAULT_OPEN):
            p = node.obj.transform.position
            r = node.obj.transform.orientation
            s = node.obj.transform.scale
            imgui.text_ansi_colored(f"position: [{round(p.x, 4)}, {round(p.y, 4)}, {round(p.z, 4)}]", 0.8, 0.8, 0.8)
            imgui.text_ansi_colored(f"rotation: [{round(r.x, 4)}, {round(r.y, 4)}, {round(r.z, 4)}]", 0.8, 0.8, 0.8)
            imgui.text_ansi_colored(f"scale: [{round(s.x, 4)}, {round(s.y, 4)}, {round(s.z, 4)}]", 0.8, 0.8, 0.8)
            for child in node.children:
                self._draw_node_gui(child)
            imgui.tree_pop()
