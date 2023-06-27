
from typing import Self

from pygame import Vector3

from geometry import Vertex


class Primitive:
    def __init__(self: Self) -> None:
        self.verts: list[Vertex] = list[Vertex]()


class Cube(Primitive):
    def __init__(self: Self, size: float) -> None:
        super().__init__()

        sh: float = size / 2

        self.verts.append(Vertex(Vector3(-sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, sh, -sh)))
        self.verts.append(Vertex(Vector3(-sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(-sh, sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, sh, -sh)))

        self.verts.append(Vertex(Vector3(-sh, -sh, sh)))
        self.verts.append(Vertex(Vector3(sh, -sh, sh)))
        self.verts.append(Vertex(Vector3(sh, sh, sh)))
        self.verts.append(Vertex(Vector3(-sh, -sh, sh)))
        self.verts.append(Vertex(Vector3(-sh, sh, sh)))
        self.verts.append(Vertex(Vector3(sh, sh, sh)))

        self.verts.append(Vertex(Vector3(-sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, -sh, sh)))
        self.verts.append(Vertex(Vector3(-sh, -sh, -sh)))
        self.verts.append(Vertex(Vector3(-sh, -sh, sh)))
        self.verts.append(Vertex(Vector3(sh, -sh, sh)))

        self.verts.append(Vertex(Vector3(-sh, sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, sh, -sh)))
        self.verts.append(Vertex(Vector3(sh, sh, sh)))
        self.verts.append(Vertex(Vector3(-sh, sh, -sh)))
        self.verts.append(Vertex(Vector3(-sh, sh, sh)))
        self.verts.append(Vertex(Vector3(sh, sh, sh)))
