

import glm

from typing import Self

from app_state import AppState
from camera import Camera
from mesh import Mesh
from primitives import Cube
from shader import Shader, ShaderType
from shader_program import ShaderProgram


class AppStateDev(AppState):
    def __init__(self: Self) -> None:
        self.mesh = None
        super().__init__()

    def init(self: Self) -> None:

        self.camera: Camera = Camera()

        self.frag_shader = Shader(ShaderType.fragment, "scene.frag")
        self.vert_shader = Shader(ShaderType.vertex, "scene.vert")
        self.frag_shader.compile()
        self.vert_shader.compile()

        self.shader_program = ShaderProgram([self.frag_shader,
                                             self.vert_shader])

        self.shader_program.compile()

        self.shader_program.use()

        self.model_pos: glm.vec3 = glm.vec3(-5, 0, 0)
        self.model_scale: glm.vec3 = glm.vec3(1, 1, 1)
        self.model_rot = glm.angleAxis(0, glm.vec3(0, 1, 0))

        self.model_transform = (glm.translate(glm.mat4(1.0), self.model_pos) *
                                glm.mat4_cast(self.model_rot) *
                                glm.scale(glm.mat4(1.0), self.model_scale))

        self.mesh = Mesh(Cube(1.0))

    def tick(self: Self, delta_ns: int) -> None:
        return super().tick(delta_ns)

    def draw(self: Self, delta_ns: int) -> None:
        # pg.gl().push(self.camera.transform)
        self.shader_program.set_mvp((self.camera.projection *
                                     self.camera.transform *
                                     self.model_transform))
        self.mesh.draw()
        # pg.gl().pop()
        return super().draw(delta_ns)
