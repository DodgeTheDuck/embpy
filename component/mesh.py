

from component.transform import TransformComponent
import pg
from typing import Self
from component.component import Component
from mesh import Mesh
from scene.scene_object import SceneObject
import OpenGL.GL as gl


class MeshComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.mesh: Mesh = None
        super().__init__(owner)
        pass

    def set_mesh(self: Self, mesh: Mesh) -> Self:
        self.mesh = mesh
        return self

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw(self: Self) -> None:
        transform = self.owner.get_component(TransformComponent)
        if transform is not None:
            pg.gl().push_mat_model(transform.as_mat4())
            pg.gl().apply_mvp(pg.gl().get_program("scene"))

            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.mesh.vao.buffer)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.mesh.ibo.buffer)

            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.mesh.texture.texture)

            gl.glDrawElements(gl.GL_TRIANGLES,
                              len(self.mesh.indices),
                              gl.GL_UNSIGNED_INT,
                              None)

            pg.gl().pop_mat_model()
        return super().draw()
