
from typing import Self

import glm
from component.component import Component
from component.transform_component import TransformComponent
from scene.scene_object import SceneObject


class RigidBodyComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        super().__init__(owner, "Rigid Body")
        self.acceleration = glm.vec3(0, 0, 0)
        self.velocity = glm.vec3(0, 0, 0)
        self.dampening = 0

    def tick(self: Self, delta: float) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            self.velocity += self.acceleration
            transform.translate(self.velocity * delta)
            self.acceleration = glm.vec3(0, 0, 0)
        return super().tick(delta)

    # TODO: work out the maff to make this work in 3 dimensions
    def impulse(self: Self, force: float, angle: float) -> Self:
        self.acceleration.x += glm.cos(angle) * force
        self.acceleration.z += glm.sin(angle) * force
