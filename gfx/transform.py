
from typing import Self

import glm


class Transform:
    def __init__(self: Self,
                 position: glm.vec3 = glm.vec3(0.0),
                 orientation: glm.vec3 = glm.vec3(0.0),
                 scale: glm.vec3 = glm.vec3(1.0)) -> None:
        self.position = position
        self.orientation = orientation
        self.scale = scale

    def as_mat4(self: Self) -> glm.mat4:
        return (glm.translate(glm.mat4(), self.position)
                * glm.mat4_cast((glm.angleAxis(self.orientation.x, glm.vec3(1, 0, 0))
                                * glm.angleAxis(self.orientation.y, glm.vec3(0, 1, 0))
                                * glm.angleAxis(self.orientation.z, glm.vec3(0, 0, 1))))
                * glm.scale(glm.mat4(), self.scale))
