from typing import Self
import OpenGL.GL as gl
from gfx.attachment import Attachment, AttachmentType
from gfx.fbo import FBO
from loaders.gltf_loader import GltfLoader
import asset.asset_manager as asset_manager
import imgui
import config


class PipelineStage:
    def __init__(self: Self, name: str) -> None:
        loader = GltfLoader("models/gltf/plane/plane.glb")
        meshes = loader.load()
        self.mesh = meshes.root.obj.meshes[0]
        self.name = name
        self.fbo = FBO()

    def add_attachment(self: Self, index: int, att_type: AttachmentType) -> None:
        self.fbo.add_attachment(index, att_type)

    def get_attachment(self: Self, index: int) -> Attachment:
        return self.fbo.attachments[index]

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

    def bind(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo.buffer)

    def unbind(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def draw_gui(self: Self) -> None:
        for att in self.fbo.attachments:
            imgui.text_colored(att.name, 0.8, 0.8, 0.8)
            imgui.image(att.texture, 128 * config.ASPECT_RATIO, 128, (1, 1), (0, 0))
