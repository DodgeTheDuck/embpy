
from math import atan2
from typing import Self

import glm
from component.component import Component
from component.transform_component import TransformComponent
from scene.scene_object import SceneObject


class RigidBodyComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        super().__init__(owner, "Rigid Body")
        self.mass = 1
        self.acceleration = glm.vec3(0, 0, 0)
        self.velocity = glm.vec3(0, 0, 0)
        self.restitution = 0

    def physics_tick(self: Self, delta: float) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            self.velocity += self.acceleration * delta
            transform.translate(self.velocity * delta)
            self.acceleration = glm.vec3(0, 0, 0)
        return super().tick(delta)

    def impulse(self: Self, force: glm.vec3) -> Self:
        if self.mass != 0:
            self.velocity += force / self.mass

    def set_mass(self: Self, mass: float) -> Self:
        self.mass = mass
        return self

    def get_restitution(self: Self) -> float:
        return self.restitution

    def set_restitution(self: Self, restitution: float) -> Self:
        self.restitution = restitution
        return self
