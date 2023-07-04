from __future__ import annotations
from typing import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scene.scene_object import SceneObject


class Component:

    def __init__(self: Self, owner: SceneObject) -> None:
        self.owner = owner

    def tick(self: Self, delta: float) -> None:
        pass

    def draw(self: Self) -> None:
        pass
