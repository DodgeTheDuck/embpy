from typing import Self
from gfx.attribute import AttributeType
from gfx.buffer_data import BufferData
from gfx.material_properties import MaterialProperties
from gfx.vao import VAO
from gfx.vbo import VBO

# TODO:
# - manage resources better; delete vert/index data after buffers created?


class Mesh:
    def __init__(self: Self,
                 buffer_data: list[BufferData],
                 n_indices: int,
                 index_type: int,
                 material_properties: MaterialProperties) -> None:
        self.vao = vao = VAO()
        self.n_indices = n_indices
        self.index_type = index_type
        self.material_properties = material_properties
        self.do_lighting = True
        self.attribute_types: list[AttributeType] = list[AttributeType]()
        vao.bind()

        for data in buffer_data:
            vbo = VBO(data.data, data.target)
            vbo.bind()
            if data.attributes:
                for attribute in data.attributes:
                    self.attribute_types.append(attribute.att_type)
                    attribute.bind()

        vao.unbind()

    def bind(self: Self) -> None:
        self.vao.bind()
        # self.material.apply()
        # if "has_tangents" in self.material.shader.uniforms:
        #     if AttributeType.TANGENT not in self.attribute_types:
        #         engine.gfx.uni_int1(self.material.shader, "has_tangents", 0)
        #     else:
        #         engine.gfx.uni_int1(self.material.shader, "has_tangents", 1)
