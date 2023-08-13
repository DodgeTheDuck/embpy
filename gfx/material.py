
from typing import Self
from webbrowser import get

from gfx.material_properties import MaterialProperties, TextureType
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
        imgui.text("Textures")
        for type in self.properties.textures:
            if imgui.collapsing_header(type.name)[0]:
                tex = self.properties.textures[type]
                imgui.image(tex.texture, 128, 128)
