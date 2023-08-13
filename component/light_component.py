
from enum import Enum
from typing import Self
import glm
from component.component import Component
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.mesh import Mesh
from gfx.shader_program import ShaderProgram
from scene.scene_object import SceneObject
import core.pg as pg
import imgui


class LightType(Enum):
    none = 0
    point = 1
    directional = 2


class LightComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.volume = NodeGraph[list[Mesh]]()
        self.color = glm.vec3(1, 1, 1)
        self.intensity = 1.0
        self.type = LightType.none
        self.attenuation = 1.0
        self.direction = glm.vec3(0, 0, 0)
        super().__init__(owner, "Light")

    def set_color(self: Self, color: glm.vec3) -> Self:
        self.color = color
        return self

    def set_intensity(self: Self, intensity: float) -> Self:
        self.intensity = intensity
        return self

    def set_attenuation(self: Self, attenuation: float) -> Self:
        self.attenuation = attenuation
        return self

    def set_type(self: Self, type: LightType) -> Self:
        self.type = type
        return self

    def set_direction(self: Self, direction: glm.vec3) -> Self:
        self.direction = direction
        return self

    def set_volume_mesh(self: Self, mesh_tree: NodeGraph[list[Mesh]]) -> Self:
        self.volume = mesh_tree
        return self

    def apply_light_properties(self: Self, shader: ShaderProgram, light_index: int) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            pg.gl().uni_vec3(shader, f"lights[{light_index}].position", transform.transform.position)
            pg.gl().uni_vec3(shader, f"lights[{light_index}].color", self.color)
            pg.gl().uni_float1(shader, f"lights[{light_index}].intensity", self.intensity)
            pg.gl().uni_float1(shader, f"lights[{light_index}].attenuation", self.attenuation)

    def apply_light_view(self: Self, shader: ShaderProgram) -> None:
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            light_proj = glm.ortho(-100, 100, -100, 100, 1, 100)
            light_view = glm.lookAt(transform.transform.position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
            pg.gl().uni_mat4(shader.program, "pv", light_proj * light_view)

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:

        col_changed, col_val = imgui.color_edit3("color", *self.color)

        if col_changed:
            self.color.x = col_val[0]
            self.color.y = col_val[1]
            self.color.z = col_val[2]

        intensity_changed, intensity_val = imgui.input_float("intensity", self.intensity)

        if intensity_changed:
            self.intensity = intensity_val

        attenuation_changed, attenuation_val = imgui.input_float("attenuation", self.attenuation)

        if attenuation_changed:
            self.attenuation = attenuation_val

        return super().draw_gui()
