from types import FunctionType
from typing import Self
import OpenGL.GL as gl
from gfx.attachment import Attachment, AttachmentType
from gfx.fbo import FBO
from gfx.shader_program import ShaderProgram
from loaders.gltf_loader import GltfLoader
import core.asset.asset_manager as asset_manager
import imgui
import config


class PipelineStageState:
    def __init__(self: Self, state_name: int, enable: bool) -> None:
        self.state_name = state_name
        self.enable = enable


class PipelineStage:
    def __init__(self: Self, name: str, default_shader: ShaderProgram = None) -> None:
        loader = GltfLoader("assets/models/rendering/plane/plane.glb")
        meshes = loader.load()
        self.default_shader = default_shader
        self.mesh = meshes.root.children[0].obj.meshes[0]
        self.name = name
        self.fbo = FBO()
        self.state_begin: FunctionType = None
        self.state_end: FunctionType = None

    def set_state_begin(self: Self, state_func: FunctionType) -> None:
        self.state_begin = state_func

    def set_state_end(self: Self, state_func: FunctionType) -> None:
        self.state_end = state_func

    def add_attachment(self: Self, index: int, att_type: AttachmentType) -> None:
        self.fbo.add_attachment(index, att_type)

    def get_attachment(self: Self, index: int) -> Attachment:
        return self.fbo.attachments[index]

    def get_default_shader(self: Self) -> ShaderProgram:
        return self.default_shader

    def render(self: Self, input_stage: Self) -> None:
        if self.default_shader is None:
            raise Exception(f"No shader bound to pipeline stage {self.name}")
        self.default_shader.use()
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, input_stage.get_attachment(0).texture)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, input_stage.get_attachment(1).texture)

        gl.glBindVertexArray(self.mesh.vao.buffer)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDrawElements(gl.GL_TRIANGLES,
                          self.mesh.n_indices,
                          self.mesh.index_type,
                          None)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def blit(self: Self) -> None:
        gl.glUseProgram(asset_manager.get_asset("fbo_blit").object.program)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.get_attachment(0).texture)
        gl.glBindVertexArray(self.mesh.vao.buffer)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDrawElements(gl.GL_TRIANGLES,
                          self.mesh.n_indices,
                          self.mesh.index_type,
                          None)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def begin_state(self: Self) -> None:
        if self.state_begin is not None:
            self.state_begin()

    def end_state(self: Self) -> None:
        if self.state_end is not None:
            self.state_end()

    def bind_fbo(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo.buffer)

    def unbind(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def draw_gui(self: Self) -> None:
        for att in self.fbo.attachments:
            imgui.text_colored(att.name, 0.8, 0.8, 0.8)
            imgui.image(att.texture, 128 * config.ASPECT_RATIO, 128, (1, 1), (0, 0))
