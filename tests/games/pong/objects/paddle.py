
from typing import Self
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType
from tests.games.pong.components.paddle_controller import PaddleController

import glm


class Paddle(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        paddle_loader: GltfLoader = GltfLoader("assets/models/cube/cube.glb")
        paddle_mesh: NodeGraph[MeshNode] = paddle_loader.load()        

        mesh_c = ModelComponent(self)
        mesh_c.set_mesh_tree(paddle_mesh)
        mesh_c.set_material(Material("basic_shading"))
        mesh_c.lit = True

        trans_c = TransformComponent(self)
        trans_c.transform.scale = glm.vec3(6, 0.8, 0.8)

        controller_c = PaddleController(self)

        self.add_component(mesh_c).add_component(trans_c).add_component(controller_c)
