
from typing import Self
from geometry import Vertex
from primitives import Primitive
from vbo import VBO


class Mesh:
    def __init__(self: Self, vertices: list[Vertex] | Primitive) -> None:
        if isinstance(vertices, Primitive):
            self.vertices: list[Vertex] = vertices.verts
        elif isinstance(vertices, list[Vertex]):
            self.vertices: list[Vertex] = vertices

        self.vbo: VBO = VBO(self.vertices)

    def draw(self: Self) -> None:
        self.vbo.draw()
