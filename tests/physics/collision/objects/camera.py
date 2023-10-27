
from typing import Self

import glm
import config
from component.camera_component import CameraComponent
from scene.scene_object import SceneObject, SceneObjectType


class Camera(SceneObject):

    def __init__(self: Self, name: str) -> None:
        super().__init__(name, SceneObjectType.ENTITY)

        cam_c = (CameraComponent(self)
                 .set_offset(glm.vec3(0, 0, 0))
                 .set_projection_perspective(config.FOV, config.ASPECT_RATIO, config.VIEW_NEAR, config.VIEW_FAR)
                 .look_at(glm.vec3(0, 0, 0))
                 .set_is_free(True))

        self.add_component(cam_c)
