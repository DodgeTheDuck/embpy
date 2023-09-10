
from enum import Enum
from typing import Self

import glm
from gfx.texture import Texture


class TextureType(Enum):
    none = 0
    albedo = 1
    metallic_roughness = 2
    normal = 3


class ScalarType(Enum):
    none = 0
    metallic = 1
    roughness = 2


class ColorType(Enum):
    none = 0
    albedo = 1


class ColorProperty:
    def __init__(self: Self, name: str, value: glm.vec3) -> None:
        self.name = name
        self.value = value


class MaterialProperties:
    def __init__(self: Self) -> None:
        self.textures = dict[TextureType, Texture]()
        self.scalars = dict[ScalarType, float]()
        self.colors = dict[ColorType, ColorProperty]()

    def add_color_property(self: Self, name: str, type: ColorType, value: glm.vec3) -> Self:
        self.colors[type] = ColorProperty(name, value)

    def get_color_property(self: Self, type: ColorType) -> ColorProperty:
        return self.colors[type]

    def set_scalar(self: Self, scalar_type: ScalarType, value: float) -> None:
        self.scalars[scalar_type] = value

    def get_scalar(self: Self, scalar_type: ScalarType) -> None:
        return self.scalars[scalar_type]

    def set_texture(self: Self, tex_type: TextureType, texture: Texture) -> None:
        self.textures[tex_type] = texture

    def get_texture(self: Self, tex_type: TextureType) -> Texture:
        return self.textures[tex_type]

    def has_texture(self: Self, tex_type: TextureType) -> bool:
        return tex_type in self.textures

    def has_color_property(self: Self, col_type: ColorType) -> bool:
        return col_type in self.colors
