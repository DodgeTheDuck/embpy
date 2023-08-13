
from typing import Self
from gfx.material_properties import MaterialProperties
from gfx.shader_program import ShaderProgram
import imgui


class Material():
    def __init__(self: Self, shader: ShaderProgram, properties: MaterialProperties) -> None:
        self.properties = properties
        self.shader = shader

    def set_shader(self: Self, shader: ShaderProgram) -> None:
        self.shader = shader

    def set_properties(self: Self, properties: MaterialProperties) -> None:
        self.properties = properties

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
