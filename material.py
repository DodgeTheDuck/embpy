from enum import Enum
from typing import Self
from gl.texture import Texture


class TextureType(Enum):
    none = 0
    diffuse = 1


class Material:
    def __init__(self: Self) -> None:
        self.textures = dict[TextureType, Texture]()
        self.col_diffuse = list[float]()

    def set_texture(self: Self,
                    tex_type: TextureType,
                    texture: Texture) -> None:
        self.textures[tex_type] = texture

    def has_texture(self: Self, tex_type: TextureType) -> bool:
        return tex_type in self.textures

    def get_texture(self: Self, tex_type: TextureType) -> Texture:
        return self.textures[tex_type]
