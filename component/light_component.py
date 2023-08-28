
from enum import Enum
from typing import Self
import glm
from component.component import Component
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.mesh import Mesh
from gfx.shader_program import ShaderProgram
from scene.scene_object import SceneObject
import core.engine as engine
import imgui
import config


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
        self.enabled = True
        self.cast_shadows = True
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

    def apply_light_view(self: Self, shader: ShaderProgram) -> None:
        if not self.enabled or not self.cast_shadows: return
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            light_proj = glm.perspective(config.FOV, config.ASPECT_RATIO, 0.01, 100)
            light_view = glm.lookAt(transform.transform.position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
            engine.gfx.uni_mat4(shader.program, "p", light_proj)
            engine.gfx.uni_mat4(shader.program, "v", light_view)

    def get_depth_bias_mvp(self: Self) -> glm.mat4:
        if not self.enabled or not self.cast_shadows: return glm.mat4()
        transform: TransformComponent = self.owner.get_component(TransformComponent)
        if transform is not None:
            bias_matrix = glm.mat4(
                0.5, 0.0, 0.0, 0.0,
                0.0, 0.5, 0.0, 0.0,
                0.0, 0.0, 0.5, 0.0,
                0.5, 0.5, 0.5, 1.0
            )
            p = glm.perspective(config.FOV, config.ASPECT_RATIO, 0.1, 25)
            v = glm.lookAt(transform.transform.position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
            return bias_matrix * p * v
        return glm.mat4()

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

        enabled_changed, enabled_val = imgui.checkbox("enabled", self.enabled)

        if enabled_changed:
            self.enabled = enabled_val

        shadow_caster_changed, shadow_caster_val = imgui.checkbox("shadow caster", self.cast_shadows)

        if shadow_caster_changed:
            self.cast_shadows = shadow_caster_val

        return super().draw_gui()
