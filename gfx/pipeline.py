
from typing import Self

from gfx.pipeline_stage import PipelineStage
from gfx.shader_program import ShaderProgram


class Pipeline:
    def __init__(self: Self) -> None:
        self.stages = dict[str, PipelineStage]()

    def add_stage(self: Self, name: str, stage: PipelineStage) -> None:
        self.stages[name] = stage

    def bind_stage(self: Self, name: str) -> None:
        self.stages[name].bind()

    def draw_stage(self: Self, name: str) -> None:
        self.stages[name].draw()

    def blit_stage(self: Self, name: str) -> None:
        self.stages[name].blit()

    def bind_textures(self: Self, name: str, shader: ShaderProgram) -> None:
        self.stages[name].bind_textures(shader)
