
from typing import Self
from gl.ibo import IBO
from gl.vbo import VBO
import OpenGL.GL as gl

# TODO:
# - move vbo setup outside of VAO


class VAO:
    def __init__(self: Self,
                 verts: list[float],
                 normals: list[float],
                 uvs: list[float],
                 indices: list[int],
                 diffuse: list[float]) -> None:

        self.ibo = IBO(indices)
        vbo_vert = VBO(verts)
        vbo_norm = VBO(normals)
        vbo_uv = VBO(uvs)
        vbo_diffuse = VBO(diffuse)

        self.buffer = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.buffer)
        vbo_vert.setup_attributes(0, 3)
        vbo_norm.setup_attributes(1, 3)
        vbo_uv.setup_attributes(2, 2)
        vbo_diffuse.setup_attributes(3, 3)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo.buffer)
        gl.glBindVertexArray(0)
