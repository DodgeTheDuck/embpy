from ast import Dict, List
from enum import Enum
from typing import Self
from gl.texture import Texture


class TextureType(Enum):
    none = 0
    albedo = 1
    metallic_roughness = 2


class Material:
    def __init__(self: Self) -> None:
        self.textures: Dict[TextureType, Texture] = {}
        self.col_albedo: List[float] = []

    def set_texture(self: Self, tex_type: TextureType, texture: Texture) -> None:
        self.textures[tex_type] = texture

    def get_texture(self: Self, tex_type: TextureType) -> Texture:
        return self.textures[tex_type]

    def has_texture(self: Self, tex_type: TextureType) -> bool:
        return tex_type in self.textures
