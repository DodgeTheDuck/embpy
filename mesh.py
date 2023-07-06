
from typing import Self
from gl.vao import VAO
from material import Material

# TODO:
# - manage resources better; delete vert/index data after buffers created?


class Mesh:
    def __init__(self: Self,
                 vertices: list[float],
                 normals: list[float],
                 uvs: list[float],
                 indices: list[int],
                 material: Material) -> None:

        self.vertices: list[float] = vertices
        self.normals: list[float] = normals
        self.uvs: list[float] = uvs
        self.indices = indices
        self.material = material

        self.vao = VAO(vertices, normals, uvs, indices, material.col_diffuse)
