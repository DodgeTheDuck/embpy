
from typing import Self

import glm
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType


class ObjSkyBox(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.SKYBOX)

        cube_loader: GltfLoader = GltfLoader("assets/models/cube/cube.glb")
        cube_mesh: NodeGraph[MeshNode] = cube_loader.load()

        trans = TransformComponent(self)
        trans.transform.position = glm.vec3(0, 0, 0)
        trans.transform.scale = glm.vec3(100, 100, 100)

        mesh = ModelComponent(self)
        mesh.set_mesh_tree(cube_mesh)
        mesh.shaded = False

        self.add_component(mesh).add_component(trans)
