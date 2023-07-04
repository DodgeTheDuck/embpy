
from typing import Self
from gl.vbo import VBO
import OpenGL.GL as gl


class VAO:
    def __init__(self: Self, verts: list[float], normals: list[float], uvs: list[float]) -> None:
        self.buffer = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.buffer)
        VBO(verts, 3, 0)
        VBO(normals, 3, 1)
        VBO(uvs, 2, 2)
