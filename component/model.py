from component.transform import TransformComponent
from material import Material, TextureType
import pg
from typing import Self
from component.component import Component
from mesh import Mesh
from scene.scene_object import SceneObject
import OpenGL.GL as gl

# TODO:
# - handle material stuff better


class ModelComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.meshes: list[Mesh]
        super().__init__(owner)
        pass

    def set_meshes(self: Self, meshes: list[Mesh]) -> Self:
        self.meshes = meshes
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw(self: Self) -> None:
        transform = self.owner.get_component(TransformComponent)
        if transform is not None:
            program = pg.gl().get_program("scene")
            pg.gl().push_mat_model(transform.as_mat4())
            pg.gl().apply_mvp(program)

            for mesh in self.meshes:
                material: Material = mesh.material
                gl.glBindVertexArray(mesh.vao.buffer)

                if material.has_texture(TextureType.diffuse):
                    gl.glUniform1i(gl.glGetUniformLocation(program,
                                                           "hasTexture"), 1)
                    texture = material.get_texture(TextureType.diffuse).texture
                    gl.glActiveTexture(gl.GL_TEXTURE0)
                    gl.glBindTexture(gl.GL_TEXTURE_2D,
                                     texture)
                else:
                    pg.gl().bind_empty_texture()

                gl.glDrawElements(gl.GL_TRIANGLES,
                                  len(mesh.vao.ibo.indices),
                                  gl.GL_UNSIGNED_INT,
                                  None)

                err: gl.GLenum
                err = gl.glGetError()
                if err != gl.GL_NO_ERROR:
                    print(f"opengl error: {err}")

            pg.gl().pop_mat_model()

        return super().draw()
