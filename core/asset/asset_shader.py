
from typing import Self
from asset.asset import Asset, AssetType
from loaders.shader_loader import ShaderLoader


class AssetShader(Asset):
    def __init__(self: Self, name: str, filepath: str) -> None:
        self.filepath = filepath
        super().__init__(name, AssetType.SHADER)

    def load(self: Self) -> Self:
        self.object = ShaderLoader(self.filepath).load()
        return self

    def draw_gui(self: Self) -> None:

        return super().draw_gui()
