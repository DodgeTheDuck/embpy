
from typing import Self

from scene.scene_graph import SceneGraph
from scene.scene_object import SceneObject, SceneObjectType


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

    def get_from_type(self: Self, type: SceneObjectType) -> list[SceneObject]:
        return self._get_from_type_recursive(self.graph.root, type, [])

    def _get_from_type_recursive(self: Self, obj: SceneObject, type: SceneObjectType, result: list[SceneObject]) -> SceneObject:
        for child in obj.children:
            if child.type == type:
                result.append(child)
            self._get_from_type_recursive(child, type, result)
        return result
