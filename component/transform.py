
from typing import Self

import glm
from component.component import Component
from scene.scene_object import SceneObject


class TransformComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.position = glm.vec3()
        self.rotation = glm.angleAxis(0, glm.vec3(0, 1, 0))
        self.scale = glm.vec3(0.2)
        super().__init__(owner)

    def as_mat4(self: Self) -> glm.mat4:
        return (glm.translate(glm.mat4(1.0), self.position) *
                glm.mat4_cast(self.rotation) *
                glm.scale(glm.mat4(1.0), self.scale))
