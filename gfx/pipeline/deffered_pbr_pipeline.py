
from typing import Self
from gfx.pipeline.pipeline import Pipeline
from gfx.pipeline.pipeline_stage import PipelineStage
from loaders.shader_loader import ShaderLoader


class DefferedPbrPipeline(Pipeline):
    def __init__(self: Self) -> None:
        super().__init__()

        geometry_loader = ShaderLoader("assets/shader/geometry.shader")
        geometry_shader = geometry_loader.load()

        light_pass_loader = ShaderLoader("assets/shader/light_pass.shader")
        light_pass_shader = light_pass_loader.load()

        shading_loader = ShaderLoader("assets/shader/shading.shader")
        shading_shader = shading_loader.load()

        blit_loader = ShaderLoader("assets/shader/fbo_draw.shader")
        blit_shader = blit_loader.load()

        self.add_stage("geometry", PipelineStage("geometry", geometry_shader, blit_shader))
        self.add_stage("light_pass", PipelineStage("light_pass", light_pass_shader, blit_shader))
        self.add_stage("shading", PipelineStage("shading", shading_shader, blit_shader))
