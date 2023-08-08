
from typing import Self

from scene.scene_object import SceneObject, SceneObjectType


class SceneGraph:
    def __init__(self: Self) -> None:
        self.root = SceneObject("scene", SceneObjectType.none)
        pass

    def tick(self: Self, delta: float) -> None:
        self.root.tick(delta)

    def draw_geometry(self: Self) -> None:
        self.root.draw_pass_geometry()

    def draw_lighting(self: Self) -> None:
        self.root.draw_pass_lighting()
