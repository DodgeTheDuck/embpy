

import math
import glm

from typing import Self

import pygame
from component.light_component import LightComponent, LightType
from gfx.pipeline.basic_shading_pipeline import BasicShadingPipeline
from gfx.mesh_node import MeshNode
import gui.gui as gui

import config

from core.app_state import AppState
from core.camera import Camera
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from loaders.gltf_loader import GltfLoader
from core.node_graph import NodeGraph
from scene.scene_object import SceneObject, SceneObjectType
import core.pg as pg
import core.engine as engine

# TODO:
# - move most of the stuff here in to the main engine


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # set up test model

        pg.gl().set_pipeline(BasicShadingPipeline())

        loader: GltfLoader = GltfLoader("models/gltf/roman_armour/armour.glb")
        armour_mesh: NodeGraph[MeshNode] = loader.load()

        armour_obj = SceneObject("test object", SceneObjectType.entity)
        mesh_c = ModelComponent(armour_obj)
        mesh_c.set_mesh_tree(armour_mesh)

        trans_c = TransformComponent(armour_obj)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        trans_c.transform.orientation = glm.vec3(0, math.pi, 0)

        armour_obj.add_component(mesh_c).add_component(trans_c)

        # set up point light

        loader: GltfLoader = GltfLoader("models/gltf/light_volumes/point_light.glb")
        light_volume: NodeGraph[MeshNode] = loader.load()

        light_obj = SceneObject("test light", SceneObjectType.light)
        light_c = LightComponent(light_obj)
        light_c.set_volume_mesh(light_volume).set_color(glm.vec3(1, 0, 0)).set_intensity(3000).set_type(LightType.point)

        light_trans_c = TransformComponent(light_obj)
        light_trans_c.transform.scale = glm.vec3(500, 500, 500)

        light_obj.add_component(light_c).add_component(light_trans_c)

        # set up dir light

        loader: GltfLoader = GltfLoader("models/gltf/plane/plane.glb")
        light_dir_volume: NodeGraph[MeshNode] = loader.load()

        light_dir_obj = SceneObject("sun", SceneObjectType.light)
        light_dir_c = LightComponent(light_dir_obj)
        light_dir_c.set_volume_mesh(light_dir_volume).set_color(glm.vec3(1, 1, 1)).set_intensity(3000).set_type(LightType.directional).set_direction(glm.vec3(0, -1, 0))
        light_dir_trans_c = TransformComponent(light_dir_obj)
        light_dir_trans_c.transform.scale = glm.vec3(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 100)
        light_dir_obj.add_component(light_dir_c).add_component(light_dir_trans_c)

        engine.scene.graph.root.add_child(armour_obj).add_child(light_obj)  # .add_child(light_dir_obj)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == BasicShadingPipeline.Stage.RENDER.value:
            pg.gl().push_mat_view(self.camera.transform)
            pg.gl().push_mat_proj(self.camera.projection)
            engine.scene.draw_geometry()
            pg.gl().pop_mat_proj
            pg.gl().pop_mat_view()
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
