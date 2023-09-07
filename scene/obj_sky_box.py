
from typing import Self

import glm
from component.sky_box_component import SkyBoxComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.cube_map import CubeMap
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType


class ObjSkyBox(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.SKYBOX)

        cube_map: CubeMap = CubeMap([
            "assets/textures/skybox/right.jpg",
            "assets/textures/skybox/left.jpg",
            "assets/textures/skybox/top.jpg",
            "assets/textures/skybox/bottom.jpg",
            "assets/textures/skybox/front.jpg",
            "assets/textures/skybox/back.jpg",
        ])

        cube_loader: GltfLoader = GltfLoader("assets/models/cube/cube.glb")
        cube_mesh: NodeGraph[MeshNode] = cube_loader.load()

        trans = TransformComponent(self)
        trans.transform.position = glm.vec3(0, 0, 0)
        trans.transform.scale = glm.vec3(100, 100, 100)

        sky_box = SkyBoxComponent(self)
        sky_box.set_mesh_tree(cube_mesh)
        sky_box.set_cube_map(cube_map)

        self.add_component(sky_box).add_component(trans)
