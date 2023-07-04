
from typing import Self

from scene.scene_graph import SceneGraph


class Scene:
    def __init__(self: Self) -> None:
        self.graph = SceneGraph()
        pass

    def tick(self: Self, delta: float) -> None:
        self.graph.tick(delta)

    def draw(self: Self, delta: float) -> None:
        self.graph.draw(delta)
