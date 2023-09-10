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

    # def draw_gui(self: Self) -> None:
    #     imgui.text(self.properties.name)
    #     imgui.separator()

    #     if len(self.properties.textures) > 0:
    #         imgui.text("Textures")
    #         for type in self.properties.textures:
    #             if imgui.collapsing_header(type.name)[0]:
    #                 tex = self.properties.textures[type]
    #                 imgui.image(tex.texture, 128, 128)

    #     imgui.text("Colors")
    #     albedo_col_changed, albedo_col_val = imgui.color_edit3(f"{self.properties.name} albedo", *self.properties.col_albedo)

    #     if albedo_col_changed:
    #         self.properties.col_albedo.x = albedo_col_val[0]
    #         self.properties.col_albedo.y = albedo_col_val[1]
    #         self.properties.col_albedo.z = albedo_col_val[2]

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
