from typing import Self
from component.component import Component
from scene.scene_object import SceneObject


class ControllerComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.move_speed = 0
        super().__init__(owner, "Controller")

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)
