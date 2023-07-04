
from typing import Self


class Rect:
    def __init__(self: Self, left: float, top: float,
                 width: float, height: float) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height


class Vector3:
    def __init__(self: Self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class Vector2:
    def __init__(self: Self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Vertex:
    def __init__(self: Self,
                 position: Vector3,
                 normal: Vector3 = None) -> None:
        self.position: Vector3 = position
        self.normal: Vector3 = normal

    def pack_pos(self: Self) -> list[float]:
        return [self.position.x, self.position.y, self.position.z]

    def pack_normal(self: Self) -> list[float]:
        return [self.normal.x, self.normal.y, self.normal.z]