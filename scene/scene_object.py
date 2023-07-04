from typing import Self, TypeVar

from component.component import Component


class SceneObject():

    T = TypeVar("T")

    def __init__(self: Self) -> None:
        self.components = list[Component]()
        self.children = list[SceneObject]()
        self.parent = None

    def init(self: Self) -> None:
        pass

    def tick(self: Self, delta: int) -> None:
        for component in self.components:
            component.tick(delta)
        for child in self.children:
            child.tick(delta)

    def draw(self: Self, delta: int) -> None:
        for component in self.components:
            component.draw()
        for child in self.children:
            child.draw(delta)

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
