from typing import Self
import glm

from numpy import matrix


class Camera:
    def __init__(self: Self) -> None:
        self.transform: matrix = glm.lookAt(glm.vec3(5, 5, 5),
                                            glm.vec3(0, 0, 0),
                                            glm.vec3(0, 1, 0))
        self.projection: matrix = glm.perspective(glm.radians(90),
                                                  1024/768,
                                                  0.1,
                                                  100)
