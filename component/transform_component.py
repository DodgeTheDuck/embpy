
from typing import Self

from component.component import Component
from scene.scene_object import SceneObject
import imgui

from gfx.transform import Transform


class TransformComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.transform: Transform = Transform()
        super().__init__(owner, "Transform")

    def draw_gui(self: Self) -> None:

        position = self.transform.position
        rotation = self.transform.orientation
        scale = self.transform.scale

        # TODO: make widget for vec3/quats etc

        if imgui.collapsing_header("Position")[0]:
            is_changed_x, value_x = imgui.input_float("x##1", position.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##1", position.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##1", position.z, step=0.01)
            if is_changed_x: position.x = value_x
            if is_changed_y: position.y = value_y
            if is_changed_z: position.z = value_z

        if imgui.collapsing_header("Orientation")[0]:
            is_changed_x, value_x = imgui.input_float("x##2", rotation.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##2", rotation.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##2", rotation.z, step=0.01)
            if is_changed_x: rotation.x = value_x
            if is_changed_y: rotation.y = value_y
            if is_changed_z: rotation.z = value_z

        if imgui.collapsing_header("Scale")[0]:
            is_changed_x, value_x = imgui.input_float("x##3", scale.x, step=0.01)
            is_changed_y, value_y = imgui.input_float("y##3", scale.y, step=0.01)
            is_changed_z, value_z = imgui.input_float("z##3", scale.z, step=0.01)
            if is_changed_x: scale.x = value_x
            if is_changed_y: scale.y = value_y
            if is_changed_z: scale.z = value_z

        return super().draw_gui()
