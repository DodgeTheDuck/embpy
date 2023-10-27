
from typing import Self
from component.hull_component import HullComponent
from scene.scene_object import SceneObject


class FloorHullComponent(HullComponent):
    def __init__(self: Self, owner: SceneObject, height: float) -> None:
        self.height = height
        super().__init__(owner)

    def set_height(self: Self, height: float) -> None:
        self.height = height
