from enum import Enum
from typing import Self, TypeVar

from component.component import Component


class SceneObjectType(Enum):
    NONE = 0
    ENTITY = 1
    LIGHT = 2


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

    def tick(self: Self, delta: int) -> None:
        for component in self.components:
            component.tick(delta)
        for child in self.children:
            child.tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        for component in self.components:
            component.draw_pass(pass_index)
        for child in self.children:
            child.draw_pass(pass_index)

    def draw_pass_lighting(self: Self) -> None:
        for component in self.components:
            component.draw_pass_lighting()
        for child in self.children:
            child.draw_pass_lighting()

    def get_component(self: Self, type: T) -> T:
        for component in self.components:
            if isinstance(component, type):
                return component
        return None

    def add_component(self: Self, component: Component) -> Self:
        self.components.append(component)
        return self

    def add_child(self: Self, child: Self) -> Self:
        self.children.append(child)
        return self
