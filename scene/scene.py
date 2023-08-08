
from typing import Self

from scene.scene_graph import SceneGraph


class Scene:
    def __init__(self: Self) -> None:
        self.graph = SceneGraph()
        pass

    def tick(self: Self, delta: float) -> None:
        self.graph.tick(delta)

    def draw_geometry(self: Self) -> None:
        self.graph.draw_geometry()

    def draw_lighting(self: Self) -> None:
        self.graph.draw_lighting()
