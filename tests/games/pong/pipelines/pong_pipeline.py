
from enum import Enum
from typing import Self
from gfx.attachment import Attachment, AttachmentType
from gfx.pipeline.pipeline import Pipeline
from gfx.pipeline.pipeline_stage import PipelineStage

import config
import OpenGL.GL as gl
import core.engine as engine
import core.asset.asset_manager as asset_manager


class PongPipeline(Pipeline):

    class Stage(Enum):
        NONE = 0
        RENDER = 1
        POST = 2

    def __init__(self: Self) -> None:
        super().__init__()

        stage_render = PipelineStage("render")
        stage_render.bind_fbo()
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

        stage_post = PipelineStage("post", asset_manager.get_asset("pong_post").object)
        stage_post.bind_fbo()
        stage_post.add_attachment(0,
                                  Attachment("color",
                                             AttachmentType.COLOR,
                                             config.WINDOW_WIDTH,
                                             config.WINDOW_HEIGHT,
                                             gl.GL_RGB,
                                             gl.GL_RGB,
                                             gl.GL_UNSIGNED_BYTE))

        stage_post.unbind()

        self.add_stage(stage_render).add_stage(stage_post)

    def begin(self: Self) -> None:
        return super().begin()

    def end(self: Self) -> None:
        err = gl.glGetError()
        if err != gl.GL_NO_ERROR:
            engine.console.write_line(f"GL_ERROR: {err}")
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        self.stages[-1].blit()
        return super().end()
