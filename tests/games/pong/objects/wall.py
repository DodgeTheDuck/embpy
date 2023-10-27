
from typing import Self
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.material_properties import ColorType
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType

import glm


class Wall(SceneObject):
    def __init__(self: Self, name: str, pos: glm.vec3) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        paddle_loader: GltfLoader = GltfLoader("assets/models/cube/cube.glb")
        paddle_mesh: NodeGraph[MeshNode] = paddle_loader.load()

        # TODO: make this less awful
        paddle_mesh.root.children[0].obj.meshes[0].material_properties.colors[ColorType.albedo].value = glm.vec3(0.4, 0.4, 0.4)

        mesh_c = ModelComponent(self)
        mesh_c.set_mesh_tree(paddle_mesh)
        mesh_c.set_material(Material("pong_scene"))
        mesh_c.lit = True

        trans_c = TransformComponent(self)
        trans_c.transform.scale = glm.vec3(0.2, 1, 30)
        trans_c.transform.position = pos

        self.add_component(mesh_c).add_component(trans_c)
