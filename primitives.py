
from typing import Self

from pygame import Vector3


class Primitive:
    def __init__(self: Self) -> None:
        self.verts: list[float] = list[float]()
        self.indices: list[int] = list[int]()


class Cube(Primitive):
    def __init__(self: Self, size: float) -> None:
        super().__init__()

        sh: float = size / 2

        self.verts.append(float(Vector3(-sh, sh, -sh)))  # 0
        self.verts.append(float(Vector3(sh, sh, -sh)))  # 1
        self.verts.append(float(Vector3(sh, sh, sh)))  # 2
        self.verts.append(float(Vector3(-sh, sh, sh)))  # 3
        self.verts.append(float(Vector3(-sh, -sh, -sh)))  # 4
        self.verts.append(float(Vector3(sh, -sh, -sh)))  # 5
        self.verts.append(float(Vector3(sh, -sh, sh)))  # 6
        self.verts.append(float(Vector3(-sh, -sh, sh)))  # 7

        self.indices = [0, 1, 2,
                        0, 3, 2,
                        0, 1, 5,
                        0, 4, 5,
                        0, 4, 3,
                        3, 7, 4,
                        3, 7, 2,
                        7, 6, 2,
                        6, 2, 1,
                        6, 5, 1,
                        7, 4, 6,
                        4, 5, 6]
