
from typing import Self

from scene.scene_object import SceneObject, SceneObjectType


class SceneGraph:
    def __init__(self: Self) -> None:
        self.root = SceneObject("scene", SceneObjectType.NONE)
        pass

    def tick(self: Self, delta: float) -> None:
        self.root.tick(delta)

    def physics_tick(self: Self, delta: float) -> None:
        self.root.physics_tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        self.root.draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        self.root.draw_gui()
