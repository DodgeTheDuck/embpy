
from typing import Self
from component.model_component import ModelComponent
from component.rigid_body_component import RigidBodyComponent
from component.sphere_hull_component import SphereHullComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.material_properties import ColorType
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType

import glm


class Ball(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        ball_loader: GltfLoader = GltfLoader("assets/models/sphere/sphere.glb")
        ball_mesh: NodeGraph[MeshNode] = ball_loader.load()

        mesh_c = ModelComponent(self)
        mesh_c.set_mesh_tree(ball_mesh)
        mesh_c.set_material(Material("basic_shading"))

        trans_c = TransformComponent(self)

        rb_c = RigidBodyComponent(self)
        hull_c = SphereHullComponent(self, 1)

        self.add_component(mesh_c).add_component(trans_c).add_component(rb_c).add_component(hull_c)

    def set_color(self: Self, color: glm.vec3) -> Self:
        self.get_component(ModelComponent).mesh_tree.root.children[0].obj.meshes[0].material_properties.colors[ColorType.albedo].value = color
        return self

    def set_radius(self: Self, radius: float) -> Self:
        trans_c = self.get_component(TransformComponent)
        trans_c.set_scale(glm.vec3(radius, radius, radius))
        hull_c = self.get_component(SphereHullComponent)
        hull_c.set_radius(radius)
        return self

    def tick(self: Self, delta: int) -> None:
        return super().tick(delta)
