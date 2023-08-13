

import math
import glm

from typing import Self

import pygame
from component.light_component import LightComponent, LightType
from gfx.pipeline.basic_shading_pipeline import BasicShadingPipeline
from gfx.mesh_node import MeshNode
import gui.gui as gui

from core.app_state import AppState
from core.camera import Camera
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from loaders.gltf_loader import GltfLoader
from core.node_graph import NodeGraph
from scene.scene_object import SceneObject, SceneObjectType
import core.pg as pg
import core.engine as engine


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # set up test model

        pg.gl().set_pipeline(BasicShadingPipeline())

        loader: GltfLoader = GltfLoader("assets/models/house/house.glb")
        armour_mesh: NodeGraph[MeshNode] = loader.load()

        armour_obj = SceneObject("test object", SceneObjectType.ENTITY)
        mesh_c = ModelComponent(armour_obj)
        mesh_c.set_mesh_tree(armour_mesh)

        trans_c = TransformComponent(armour_obj)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        trans_c.transform.scale = glm.vec3(10, 10, 10)
        trans_c.transform.orientation = glm.vec3(0, math.pi, 0)

        armour_obj.add_component(mesh_c).add_component(trans_c)

        # set up point light 1

        light_obj = SceneObject("test light 1", SceneObjectType.LIGHT)
        light_c = LightComponent(light_obj)
        light_c.set_color(glm.vec3(1, 1, 1)).set_intensity(3000).set_attenuation(5).set_type(LightType.point)

        light_trans_c = TransformComponent(light_obj)
        light_trans_c.transform.position = glm.vec3(0, 50, -50)

        light_obj.add_component(light_c).add_component(light_trans_c)

        # set up point light 2

        light_obj_2 = SceneObject("test light 2", SceneObjectType.LIGHT)
        light_c_2 = LightComponent(light_obj_2)
        light_c_2.set_color(glm.vec3(1, 0, 0)).set_intensity(3000).set_attenuation(5).set_type(LightType.point)

        light_trans_c_2 = TransformComponent(light_obj_2)
        light_trans_c_2.transform.position = glm.vec3(50, 50, -50)

        light_obj_2.add_component(light_c_2).add_component(light_trans_c_2)

        engine.scene.graph.root.add_child(armour_obj).add_child(light_obj).add_child(light_obj_2)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == BasicShadingPipeline.Stage.RENDER.value:
            pg.gl().push_mat_view(self.camera.transform)
            pg.gl().push_mat_proj(self.camera.projection)
            engine.scene.draw_pass(pass_index)
            pg.gl().pop_mat_proj
            pg.gl().pop_mat_view()
            pass
        if pass_index == BasicShadingPipeline.Stage.SHADOW.value:
            lights = engine.scene.get_from_type(SceneObjectType.LIGHT)
            depth_map = pg.gl().get_active_pipeline().get_active_stage().default_shader
            depth_map.use()
            for light in lights:
                light_c = light.get_component(LightComponent)
                if light_c is not None:
                    light_c.apply_light_view(depth_map)
                    engine.scene.draw_pass(pass_index)
            pass
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        gui.scene_graph(engine.scene.graph)
        gui.object_properties()
        return super().draw_gui()

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                self.camera.mouse_look()
                pass
        return super().event(event)
