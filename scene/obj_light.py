
from typing import Self
from scene.scene_object import SceneObject


class ObjLight(SceneObject):
    def __init__(self: Self, name: str) -> None:
        super().__init__(name)
