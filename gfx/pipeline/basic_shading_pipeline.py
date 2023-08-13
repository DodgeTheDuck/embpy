
from enum import Enum
from typing import Self

import config
from gfx.attachment import Attachment, AttachmentType
from gfx.pipeline.pipeline import Pipeline
from gfx.pipeline.pipeline_stage import PipelineStage
import OpenGL.GL as gl


class BasicShadingPipeline(Pipeline):

    class Stage(Enum):
        NONE = 0
        RENDER = 1

    def __init__(self: Self) -> None:
        super().__init__()

        stage_render = PipelineStage("render")
        stage_render.bind()
        stage_render.add_attachment(0,
                                    Attachment("color",
                                               AttachmentType.COLOR,
                                               config.WINDOW_WIDTH,
                                               config.WINDOW_HEIGHT,
                                               gl.GL_RGB,
                                               gl.GL_RGB,
                                               gl.GL_UNSIGNED_BYTE))
        stage_render.add_attachment(0,
                                    Attachment("depth",
                                               AttachmentType.DEPTH,
                                               config.WINDOW_WIDTH,
                                               config.WINDOW_HEIGHT,
                                               gl.GL_DEPTH_COMPONENT24,
                                               gl.GL_DEPTH_COMPONENT,
                                               gl.GL_FLOAT))
        stage_render.unbind()

        self.add_stage(stage_render)

    def end(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        self.stages[0].blit()
        return super().end()
