
from typing import Self

import glm
from component.component import Component
from scene.scene_object import SceneObject
import imgui


class TransformComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.position = glm.vec3()
        self.orientation = glm.vec3()
        self.scale = glm.vec3(1.0)
        super().__init__(owner, "Transform")

    def as_mat4(self: Self) -> glm.mat4:
        return (glm.translate(glm.mat4(1.0), self.position)
                * glm.mat4_cast((glm.angleAxis(self.orientation.x, glm.vec3(1, 0, 0))
                                 * glm.angleAxis(self.orientation.y, glm.vec3(0, 1, 0))
                                 * glm.angleAxis(self.orientation.z, glm.vec3(0, 0, 1))))
                * glm.scale(glm.mat4(1.0), self.scale))

    def gui(self: Self) -> None:

        position = self.position
        rotation = self.orientation
        scale = self.scale

        # TODO: make widget for vec3/quats etc

        if imgui.collapsing_header("Position"):
            is_changed_x, value_x = imgui.input_float("x##1", position.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##1", position.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##1", position.z, step=0.01)
            if is_changed_x: position.x = value_x
            if is_changed_y: position.y = value_y
            if is_changed_z: position.z = value_z

        if imgui.collapsing_header("Orientation"):
            is_changed_x, value_x = imgui.input_float("x##2", rotation.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##2", rotation.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##2", rotation.z, step=0.01)
            if is_changed_x: rotation.x = value_x
            if is_changed_y: rotation.y = value_y
            if is_changed_z: rotation.z = value_z

        if imgui.collapsing_header("Scale"):
            is_changed_x, value_x = imgui.input_float("x##3", scale.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##3", scale.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##3", scale.z, step=0.01)
            if is_changed_x: scale.x = value_x
            if is_changed_y: scale.y = value_y
            if is_changed_z: scale.z = value_z

        return super().gui()
