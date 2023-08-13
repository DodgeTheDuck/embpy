
from typing import Self
from core.asset.asset import Asset, AssetType
from gfx.texture import Sampler, Texture
import OpenGL.GL as gl


class AssetTexture(Asset):
    def __init__(self: Self, name: str, filepath: str) -> None:
        self.filepath = filepath
        super().__init__(name, AssetType.TEXTURE)

    def load(self: Self) -> Self:
        sampler = Sampler()
        sampler.target = gl.GL_TEXTURE_2D
        sampler.tex_mag_filter = gl.GL_NEAREST
        sampler.tex_min_filter = gl.GL_NEAREST
        sampler.tex_wrap_s = gl.GL_CLAMP
        sampler.tex_wrap_t = gl.GL_CLAMP
        self.object = Texture(self.filepath, sampler)
        return self

    def draw_gui(self: Self) -> None:

        return super().draw_gui()
