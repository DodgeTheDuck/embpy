from component.transform_component import TransformComponent
from gfx.material_properties import MaterialProperties, TextureType
from gfx.mesh_node import MeshNode
from core.node_graph import Node, NodeGraph
import core.pg as pg
from typing import Self
from component.component import Component
from scene.scene_object import SceneObject
import OpenGL.GL as gl
import imgui

# TODO:
# - handle material stuff better


class ModelComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.mesh_tree: NodeGraph[MeshNode] = None
        super().__init__(owner, "Model")
        pass

    def set_mesh_tree(self: Self, mesh_tree: NodeGraph[MeshNode]) -> Self:
        self.mesh_tree = mesh_tree
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw_pass_geometry(self: Self) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:

            pg.gl().push_mat_model(transform.transform.as_mat4())
            # gl.glUniform1i(shader.get_uniform_loc("albedo"), 0)

            self._draw_node(self.mesh_tree.root)

            pg.gl().pop_mat_model()

        return super().draw_pass_geometry()

    def _draw_node(self: Self, node: Node[MeshNode]) -> None:

        # apply node transform
        pg.gl().push_mat_model(node.obj.transform.as_mat4())

        for mesh in node.obj.meshes:
            mat_properties, shader = mesh.material.properties, mesh.material.shader
            # apply material shader
            shader.use()
            # send current mvp state to shader
            pg.gl().apply_mvp(shader.program)
            # bind mesh VAO
            mesh.vao.bind()

            # bind material textures
            if mat_properties.has_texture(TextureType.albedo):
                texture = mat_properties.get_texture(TextureType.albedo).texture
                gl.glActiveTexture(gl.GL_TEXTURE0)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            if mat_properties.has_texture(TextureType.metallic_roughness):
                texture = mat_properties.get_texture(TextureType.metallic_roughness).texture
                gl.glActiveTexture(gl.GL_TEXTURE1)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            if mat_properties.has_texture(TextureType.normal):
                texture = mat_properties.get_texture(TextureType.normal).texture
                gl.glActiveTexture(gl.GL_TEXTURE2)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

            # draw mesh
            gl.glDrawElements(gl.GL_TRIANGLES,
                              mesh.n_indices,
                              mesh.index_type,
                              None)

        # draw rest of node tree
        for child in node.children:
            self._draw_node(child)

        # pop node transform
        pg.gl().pop_mat_model()

    def gui(self: Self) -> None:
        if imgui.collapsing_header("Meshes")[0]:
            self._draw_node_gui(self.mesh_tree.root)
        if imgui.collapsing_header("Materials")[0]:
            mats: list[MaterialProperties] = []
            self._get_materials(self.mesh_tree.root, mats)
            for mat in mats:
                imgui.text_ansi(mat.name)
        return super().gui()

    def _get_materials(self: Self, node: Node[MeshNode], materials: list[MaterialProperties]) -> None:
        for mesh in node.obj.meshes:
            materials.append(mesh.material_properties)
        for child in node.children:
            self._get_materials(child, materials)

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
