
from typing import Self
import glm

import pygame
from component.controller_component import ControllerComponent
from component.transform_component import TransformComponent
from scene.scene_object import SceneObject


class PaddleController(ControllerComponent):
    def __init__(self: Self, owner: SceneObject) -> None:
        super().__init__(owner)
        self.move_speed = 10

    def tick(self: Self, delta: float) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            keys: list[int] = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                transform.translate(glm.vec3(-self.move_speed * delta, 0, 0))
            if keys[pygame.K_d]:
                transform.translate(glm.vec3(+self.move_speed * delta, 0, 0))
        return super().tick(delta)
