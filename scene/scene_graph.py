
from typing import Self

from scene.scene_object import SceneObject


class SceneGraph:
    def __init__(self: Self) -> None:
        self.root = SceneObject()
        pass

    def tick(self: Self, delta: float) -> None:
        self.root.tick(delta)

    def draw(self: Self, delta: float) -> None:
        self.root.draw(delta)
