
from typing import Self
from component.hull_component import HullComponent
from scene.scene_object import SceneObject


class SphereHullComponent(HullComponent):
    def __init__(self: Self, owner: SceneObject, radius: float) -> None:
        self.radius = radius
        super().__init__(owner)

    def set_radius(self: Self, radius: float) -> None:
        self.radius = radius
