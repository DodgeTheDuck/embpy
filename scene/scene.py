
from typing import Self, TypeVar
from component.component import Component
from gfx.camera_manager import CameraManager
from gfx.light_manager import LightManager
from scene.scene_graph import SceneGraph
from scene.scene_object import SceneObject, SceneObjectType


T = TypeVar("T")


class Scene:
    def __init__(self: Self) -> None:
        self.graph = SceneGraph()
        self.light_manager = LightManager()
        self.camera_manager = CameraManager()

    def tick(self: Self, delta: float) -> None:
        self.graph.tick(delta)

    def physics_tick(self: Self, delta: float) -> None:
        self.graph.physics_tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        self.graph.draw_pass(pass_index)

    def get_from_component_type(self: Self, type: T) -> list[Component]:
        return self._get_from_component_type_recursive(self.graph.root, type, [])

    def _get_from_component_type_recursive(self: Self, obj: SceneObject, type: T, result: list[Component]) -> list[Component]:
        component = obj.get_component(type)
        if component is not None:
            result.append(component)
        for child in obj.children:
            self._get_from_component_type_recursive(child, type, result)
        return result

    def get_from_type(self: Self, type: SceneObjectType) -> list[SceneObject]:
        return self._get_from_type_recursive(self.graph.root, type, [])

    def _get_from_type_recursive(self: Self, obj: SceneObject, type: SceneObjectType, result: list[SceneObject]) -> list[SceneObject]:
        if obj.type == type:
            result.append(obj)
        for child in obj.children:
            # if child.type == type: # NOTE: I think this isn't needed...
            #     result.append(child)
            self._get_from_type_recursive(child, type, result)
        return result
