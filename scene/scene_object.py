from enum import Enum
from typing import Self, TypeVar

from component.component import Component


class SceneObjectType(Enum):
    NONE = 0
    ENTITY = 1
    LIGHT = 2
    SKYBOX = 3


class SceneObject():

    T = TypeVar("T")

    def __init__(self: Self, name: str, type: SceneObjectType) -> None:
        self.components = list[Component]()
        self.children = list[SceneObject]()
        self.name = name
        self.parent = None
        self.type = type

    def init(self: Self) -> None:
        pass

    def tick(self: Self, delta: float) -> None:
        for component in self.components:
            component.tick(delta)
        for child in self.children:
            child.tick(delta)

    def physics_tick(self: Self, delta: float) -> None:
        for component in self.components:
            component.physics_tick(delta)
        for child in self.children:
            child.physics_tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        for component in self.components:
            component.draw_pass(pass_index)
        for child in self.children:
            child.draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        for component in self.components:
            component.draw_gui()
        for child in self.children:
            child.draw_gui()

    def get_component(self: Self, type: T) -> T:
        for component in self.components:
            if isinstance(component, type):
                return component
        return None

    def get_components(self: Self, type: T) -> list[T]:
        result = []
        for component in self.components:
            if isinstance(component, type):
                result.append(component)
        return result

    def add_component(self: Self, component: Component) -> Self:
        self.components.append(component)
        return self

    def add_child(self: Self, child: Self) -> Self:
        self.children.append(child)
        return self
