from ast import Dict, List
from enum import Enum
from typing import Self
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


class MaterialProperties:
    def __init__(self: Self) -> None:
        self.textures: Dict[TextureType, Texture] = {}
        self.name = ""
        self.scalars: Dict[ScalarType, float] = {}
        self.col_albedo: List[float] = []

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
