
from abc import abstractmethod
from typing import Self

from scene.scene_object import SceneObject


class Solver:
    def __init__(self: Self) -> None:
        pass

    @abstractmethod
    def solve(self: Self, obj: SceneObject, delta: float) -> None:
        pass
