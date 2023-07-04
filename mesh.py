
from typing import Self
from gl.ibo import IBO
from gl.texture import Texture
from gl.vao import VAO

# TODO:
# - manage resources better; delete vert/index data after buffers created?


class Mesh:
    def __init__(self: Self,
                 vertices: list[float],
                 normals: list[float],
                 uvs: list[float],
                 indices: list[int],
                 texture: Texture) -> None:

        self.vertices: list[float] = vertices
        self.normals: list[float] = normals
        self.uvs: list[float] = uvs
        self.indices = indices
        self.texture = texture

        self.vao = VAO(vertices, normals, self.uvs)
        self.ibo: IBO = IBO(self.indices)
