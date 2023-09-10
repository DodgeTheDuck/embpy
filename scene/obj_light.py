
from typing import Self

import glm
from component.light_component import LightComponent, LightType
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType


class ObjLight(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.LIGHT)

        test_light_loader: GltfLoader = GltfLoader("assets/models/light_bulb/bulb.glb")
        test_light_mesh: NodeGraph[MeshNode] = test_light_loader.load()

        light_c = LightComponent(self)
        light_c.set_color(glm.vec3(1, 1, 1)).set_intensity(400).set_attenuation(3).set_type(LightType.point)

        light_trans_c = TransformComponent(self)
        light_trans_c.transform.position = glm.vec3(0, 10, 0)
        light_trans_c.transform.scale = glm.vec3(10, 10, 10)

        light_mesh_c = ModelComponent(self)
        light_mesh_c.set_mesh_tree(test_light_mesh)
        light_mesh_c.set_material(Material("basic_shading"))
        light_mesh_c.lit = False

        self.add_component(light_c).add_component(light_trans_c).add_component(light_mesh_c)
