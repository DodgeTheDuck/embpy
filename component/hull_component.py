
from typing import Self
from component.component import Component
from scene.scene_object import SceneObject


class HullComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        super().__init__(owner, "Rigid Body")

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def physics_tick(self: Self, delta: float) -> None:
        pass
