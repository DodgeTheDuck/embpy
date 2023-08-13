
from typing import Self

from gfx.buffer_data import BufferData
from gfx.material import Material
from gfx.vao import VAO
from gfx.vbo import VBO

# TODO:
# - manage resources better; delete vert/index data after buffers created?


class Mesh:
    def __init__(self: Self,
                 buffer_data: list[BufferData],
                 n_indices: int,
                 index_type: int,
                 material: Material) -> None:
        self.vao = vao = VAO()
        self.n_indices = n_indices
        self.index_type = index_type
        self.material = material
        vao.bind()

        for data in buffer_data:
            vbo = VBO(data.data, data.target)
            vbo.bind()
            if data.attributes:
                for attribute in data.attributes:
                    attribute.bind()

        vao.unbind()
