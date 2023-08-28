from component.light_component import LightComponent
from component.transform_component import TransformComponent
import core.engine as engine

from typing import Self
from scene.obj_light import ObjLight
from scene.scene_object import SceneObjectType


class LightManager:
    def __init__(self: Self) -> None:
        self.__light_cache = list[ObjLight]()

    def cache_lights(self: Self) -> None:
        self.__light_cache = engine.scene.get_from_type(SceneObjectType.LIGHT)

    def apply_lights(self: Self) -> None:
        for index, light_obj in enumerate(self.__light_cache):
            transform_component: TransformComponent = light_obj.get_component(TransformComponent)
            light_component: LightComponent = light_obj.get_component(LightComponent)
            shader = engine.gfx.get_active_shader_program()
            engine.gfx.uni_vec3(shader, f"lights[{index}].position", transform_component.transform.position)
            engine.gfx.uni_vec3(shader, f"lights[{index}].color", light_component.color)
            engine.gfx.uni_float1(shader, f"lights[{index}].intensity", light_component.intensity if light_component.enabled else 0)
            engine.gfx.uni_float1(shader, f"lights[{index}].attenuation", light_component.attenuation)
