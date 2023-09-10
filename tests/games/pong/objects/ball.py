
from typing import Self
from component.model_component import ModelComponent
from component.rigid_body import RigidBodyComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType

import math
import random
import glm
import core.asset.asset_manager as asset_manager


class Ball(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        self.speed_multiplier = 1.1

        ball_loader: GltfLoader = GltfLoader("assets/models/sphere/sphere.glb")
        ball_mesh: NodeGraph[MeshNode] = ball_loader.load()

        mesh_c = ModelComponent(self)
        mesh_c.set_mesh_tree(ball_mesh)
        mesh_c.set_material(Material("basic_shading"))
        mesh_c.lit = True

        trans_c = TransformComponent(self)
        trans_c.transform.scale = glm.vec3(1, 1, 1)

        phys_c = RigidBodyComponent(self)
        # phys_c.impulse(2, random.random() * math.pi * 2)
        phys_c.impulse(4, math.pi / 2 + 0.4)

        self.add_component(mesh_c).add_component(trans_c).add_component(phys_c)

    def tick(self: Self, delta: int) -> None:
        transform: TransformComponent = self.get_component(TransformComponent)
        body: RigidBodyComponent = self.get_component(RigidBodyComponent)
        if transform is not None:
            # paddle collision
            if transform.transform.position.z <= -10:
                vel: float = abs(glm.length(body.velocity)) * self.speed_multiplier
                body.velocity.z = 0
                transform.transform.position.z = -9.95
                body.impulse(vel, math.pi / 2)
            if transform.transform.position.z >= 10:
                vel: float = abs(glm.length(body.velocity)) * self.speed_multiplier
                body.velocity.z = 0
                transform.transform.position.z = 9.95
                body.impulse(vel, math.pi * 1.5)

            # wall collision
            if transform.transform.position.x <= -10:
                vel: float = abs(glm.length(body.velocity))
                body.velocity.x = 0
                transform.transform.position.x = -9.95
                body.impulse(vel, 0)
            if transform.transform.position.x >= 10:
                vel: float = abs(glm.length(body.velocity))
                body.velocity.x = 0
                transform.transform.position.x = 9.95
                body.impulse(vel, -math.pi)

        return super().tick(delta)
