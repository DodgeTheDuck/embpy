
from typing import Generic, Self, TypeVar


T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self: Self, obj: T, parent: Self) -> None:
        self.obj = obj
        self.children: list[Node[T]] = list[Node[T]]()
        self.parent: Node[T] = None


class NodeGraph(Generic[T]):
    def __init__(self: Self) -> None:
        self.root: Node[T] = Node[T](None, None)

    def set_root(self: Self, obj: T) -> None:
        self.root = Node[T](obj)

    def add_node(self: Self, obj: T, parent: Node[T] | None) -> Node[T]:
        if parent is None:
            self.root = Node[T](obj, None)
            return self.root
        else:
            child = Node[T](obj, parent)
            parent.children.append(child)
            return child
