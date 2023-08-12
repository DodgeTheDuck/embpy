
from typing import Self
import OpenGL.GL as gl
from gfx.fbo import FBO
from gfx.shader_program import ShaderProgram
from loaders.gltf_loader import GltfLoader


class PipelineStage:
    def __init__(self: Self, name: str, draw_shader: ShaderProgram, blit_shader: ShaderProgram) -> None:
        self.blit_shader = blit_shader
        self.draw_shader = draw_shader
        self.name = name
        loader = GltfLoader("models/gltf/plane/plane.glb")
        meshes = loader.load()
        self.mesh = meshes.root.obj.meshes[0]
        self.fbo = FBO()

    def bind(self: Self) -> None:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo.buffer)

    def bind_textures(self: Self, shader: ShaderProgram) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.fbo.textures[0])
        gl.glUniform1i(shader.uniforms["texPosition"], 0)

        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.fbo.textures[1])
        gl.glUniform1i(shader.uniforms["texNormal"], 1)

        gl.glActiveTexture(gl.GL_TEXTURE2)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.fbo.textures[2])
        gl.glUniform1i(shader.uniforms["texAlbedo"], 2)

        gl.glActiveTexture(gl.GL_TEXTURE3)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.fbo.textures[3])
        gl.glUniform1i(shader.uniforms["texMetallicRoughness"], 3)

    def draw(self: Self) -> None:
        gl.glUseProgram(self.draw_shader.program)
        gl.glBindVertexArray(self.mesh.vao.buffer)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDrawElements(gl.GL_TRIANGLES,
                          self.mesh.n_indices,
                          self.mesh.index_type,
                          None)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def blit(self: Self) -> None:
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.fbo.textures[0])
        gl.glUseProgram(self.blit_shader.program)
        gl.glBindVertexArray(self.mesh.vao.buffer)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDrawElements(gl.GL_TRIANGLES,
                          self.mesh.n_indices,
                          self.mesh.index_type,
                          None)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def gui(self: Self) -> None:
        pass
