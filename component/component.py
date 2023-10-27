from __future__ import annotations
from typing import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scene.scene_object import SceneObject


class Component:

    def __init__(self: Self, owner: SceneObject, name: str) -> None:
        self.owner = owner
        self.name = name

    def tick(self: Self, delta: float) -> None:
        pass

    def physics_tick(self: Self, delta: float) -> None:
        pass

    def draw_pass(self: Self, pass_index: int) -> None:
        pass

    def draw_gui(self: Self) -> None:
        pass
