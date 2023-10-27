
from typing import Self
from component.model_component import ModelComponent
from component.rigid_body_component import RigidBodyComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.material import Material
from gfx.material_properties import ColorType
from gfx.mesh_node import MeshNode
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType

import math
import glm


class Ball(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        self.speed_multiplier = 1.1

        ball_loader: GltfLoader = GltfLoader("assets/models/sphere/sphere.glb")
        ball_mesh: NodeGraph[MeshNode] = ball_loader.load()
        # TODO: make this less awful
        ball_mesh.root.children[0].obj.meshes[0].material_properties.colors[ColorType.albedo].value = glm.vec3(0, 0, 0)

        mesh_c = ModelComponent(self)
        mesh_c.set_mesh_tree(ball_mesh)
        mesh_c.set_material(Material("pong_scene"))

        trans_c = TransformComponent(self)
        trans_c.transform.scale = glm.vec3(1, 1, 1)

        phys_c = RigidBodyComponent(self)
        # phys_c.impulse(2, random.random() * math.pi * 2)
        # phys_c.impulse(4, math.pi / 2 + 0.4)
        phys_c.impulse(12, math.pi + 0.2)

        self.add_component(mesh_c).add_component(trans_c).add_component(phys_c)

    def tick(self: Self, delta: int) -> None:
        transform: TransformComponent = self.get_component(TransformComponent)
        body: RigidBodyComponent = self.get_component(RigidBodyComponent)
        if transform is not None:
            # paddle collision
            if transform.transform.position.z <= -10:
                vel: float = abs(glm.length(body.velocity))  # * self.speed_multiplier
                # body.velocity.z = 0
                transform.transform.position.z = -9.5
                body.impulse(vel, math.pi / 2)
            if transform.transform.position.z >= 10:
                vel: float = abs(glm.length(body.velocity))  # * self.speed_multiplier
                # body.velocity.z = 0
                transform.transform.position.z = 9.5
                body.impulse(vel, math.pi * 1.5)

            # wall collision
            if transform.transform.position.x <= -30:
                vel: float = abs(glm.length(body.velocity))
                # body.velocity.x = 0
                transform.transform.position.x = -29.5
                body.impulse(vel, 0)
            if transform.transform.position.x >= 30:
                vel: float = abs(glm.length(body.velocity))
                # body.velocity.x = 0
                transform.transform.position.x = 29.5
                body.impulse(vel, -math.pi)

        return super().tick(delta)
