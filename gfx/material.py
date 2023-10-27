from typing import Self
from gfx.material_properties import ColorType, MaterialProperties, TextureType
from gfx.shader_program import ShaderProgram

import core.asset.asset_manager as asset_manager
import OpenGL.GL as gl
import core.engine as engine


class Material():
    def __init__(self: Self, shader_name: str) -> None:
        self.name = ""
        self.shader = asset_manager.instantiate_asset(shader_name).object
        self.is_lit = True

    def set_shader(self: Self, shader: ShaderProgram) -> None:
        self.shader = shader

    def use(self: Self) -> None:
        self.shader.use()

    def apply_properties(self: Self, properties: MaterialProperties) -> None:
        if self.shader is None:
            raise Exception("Applying material with no shader")

        self.__apply_texture(TextureType.albedo, 0, properties)
        self.__apply_texture(TextureType.metallic_roughness, 1, properties)
        self.__apply_texture(TextureType.normal, 2, properties)

        self.__apply_color(ColorType.albedo, properties)

    def __apply_texture(self: Self, texture_type: TextureType, index: int, properties: MaterialProperties) -> None:
        if properties.has_texture(texture_type):
            properties.get_texture(texture_type).bind(index)
        else:
            gl.glActiveTexture(gl.GL_TEXTURE0 + index)
            gl.glBindTexture(gl.GL_TEXTURE_2D, asset_manager.get_asset("empty_tex").object.texture)

    def __apply_color(self: Self, color_type: ColorType, properties: MaterialProperties) -> None:
        if properties.has_color_property(color_type):
            color_property = properties.get_color_property(color_type)
            engine.gfx.uni_vec3(self.shader, color_property.name, color_property.value)
