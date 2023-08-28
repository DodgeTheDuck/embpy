import imgui
import glm
import core.asset.asset_manager as asset_manager
import OpenGL.GL as gl
import core.engine as engine

from enum import Enum
from typing import Self
from gfx.shader_program import ShaderProgram
from gfx.texture_2d import Texture2D


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


class Material():
    def __init__(self: Self) -> None:
        self.name = ""
        self.shader = None
        self.textures = dict[TextureType, Texture2D]()
        self.scalars = dict[ScalarType, float]()
        self.colors = dict[ColorType, ColorProperty]()

    def add_color_property(self: Self, name: str, type: ColorType, value: glm.vec3) -> Self:
        self.colors[type] = ColorProperty(name, value)

    def set_shader(self: Self, shader: ShaderProgram) -> None:
        self.shader = shader

    def set_scalar(self: Self, scalar_type: ScalarType, value: float) -> None:
        self.scalars[scalar_type] = value

    def get_scalar(self: Self, scalar_type: ScalarType) -> None:
        return self.scalars[scalar_type]

    def set_texture(self: Self, tex_type: TextureType, texture: Texture2D) -> None:
        self.textures[tex_type] = texture

    def get_texture(self: Self, tex_type: TextureType) -> Texture2D:
        return self.textures[tex_type]

    def has_texture(self: Self, tex_type: TextureType) -> bool:
        return tex_type in self.textures

    def apply(self: Self) -> None:
        if self.shader is None:
            raise Exception("Applying material with no shader")

        self.shader.use()

        self.__apply_texture(TextureType.albedo, 0)
        self.__apply_texture(TextureType.metallic_roughness, 1)
        self.__apply_texture(TextureType.normal, 2)

        self.__apply_color(ColorType.albedo)

    def draw_gui(self: Self) -> None:
        imgui.text(self.properties.name)
        imgui.separator()

        if len(self.properties.textures) > 0:
            imgui.text("Textures")
            for type in self.properties.textures:
                if imgui.collapsing_header(type.name)[0]:
                    tex = self.properties.textures[type]
                    imgui.image(tex.texture, 128, 128)

        imgui.text("Colors")
        albedo_col_changed, albedo_col_val = imgui.color_edit3(f"{self.properties.name} albedo", *self.properties.col_albedo)

        if albedo_col_changed:
            self.properties.col_albedo.x = albedo_col_val[0]
            self.properties.col_albedo.y = albedo_col_val[1]
            self.properties.col_albedo.z = albedo_col_val[2]

    def __apply_texture(self: Self, texture_type: TextureType, index: int) -> None:
        if self.has_texture(texture_type):
            gl.glActiveTexture(gl.GL_TEXTURE0 + index)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.textures[texture_type].texture)
        else:
            gl.glActiveTexture(gl.GL_TEXTURE0 + index)
            gl.glBindTexture(gl.GL_TEXTURE_2D, asset_manager.get_asset("empty_tex").object.texture)

    def __apply_color(self: Self, color_type: ColorType) -> None:
        color_property: ColorProperty = self.colors[color_type]
        engine.gfx.uni_vec3(self.shader, color_property.name, color_property.value)
