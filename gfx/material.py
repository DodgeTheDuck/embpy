
from typing import Self

from gfx.material_properties import MaterialProperties
from gfx.shader_program import ShaderProgram


class Material():
    def __init__(self: Self, shader: ShaderProgram, properties: MaterialProperties) -> None:
        self.properties = properties
        self.shader = shader

    def set_shader(self: Self, shader: ShaderProgram) -> None:
        self.shader = shader

    def set_properties(self: Self, properties: MaterialProperties) -> None:
        self.properties = properties
