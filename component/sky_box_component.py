import imgui
import core.engine as engine

from component.transform_component import TransformComponent
from gfx.cube_map import CubeMap
from gfx.gfx import GlConstants
from gfx.material import Material, TextureType
from gfx.mesh_node import MeshNode
from core.node_graph import Node, NodeGraph
from typing import Self
from component.component import Component
from scene.scene_object import SceneObject


class SkyBoxComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.mesh_tree: NodeGraph[MeshNode] = None
        self.cube_map: CubeMap = None
        self.material = Material("skybox")
        self.material.is_lit = False
        self.shaded = True
        super().__init__(owner, "Model")
        pass

    def set_mesh_tree(self: Self, mesh_tree: NodeGraph[MeshNode]) -> Self:
        self.mesh_tree = mesh_tree
        return self

    # TODO: this is temp while i just try and get fookin skyboxes working
    def set_cube_map(self: Self, cube_map: CubeMap) -> Self:
        self.cube_map = cube_map
        self.mesh_tree.root.children[0].obj.meshes[0].material_properties.set_texture(TextureType.albedo, cube_map)
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        engine.gfx.depth_function(GlConstants.gl_lequal)
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            engine.gfx.push_mat_model(transform.transform.as_mat4())
            engine.gfx.draw_mesh_tree(self.mesh_tree.root, self.material)
            engine.gfx.pop_mat_model()
        engine.gfx.depth_function(GlConstants.gl_less)
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:

        shaded_changed, shaded_val = imgui.checkbox("shaded", self.shaded)

        if shaded_changed:
            self.shaded = shaded_val

        if imgui.collapsing_header("Nodes")[0]:
            self._draw_node_gui(self.mesh_tree.root)
        if imgui.collapsing_header("Materials")[0]:
            mats: list[Material] = []
            self._get_materials(self.mesh_tree.root, mats)
            for mat in mats:
                mat.draw_gui()

        return super().draw_gui()

    def _get_materials(self: Self, node: Node[MeshNode], materials: list[Material]) -> None:
        for mesh in node.obj.meshes:
            materials.append(mesh.material)
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
