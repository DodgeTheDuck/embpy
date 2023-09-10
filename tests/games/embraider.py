import math
from component.camera_component import CameraComponent
from component.light_component import LightComponent, LightType
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from core.node_graph import NodeGraph
from gfx.mesh_node import MeshNode
from typing import Self
from gfx.pipeline.forward_shaded_pipeline import ForwardShadedPipeline
from core.app_state import AppState
from loaders.gltf_loader import GltfLoader
from scene.scene_object import SceneObject, SceneObjectType

import glm
import pygame
import gui.gui as gui
import core.engine as engine
import config


class Embraider(AppState):
    def init(self: Self) -> None:
        engine.gfx.set_pipeline(ForwardShadedPipeline())

        test_obj_loader: GltfLoader = GltfLoader("assets/models/lara croft/lara.glb")
        test_obj_mesh: NodeGraph[MeshNode] = test_obj_loader.load()

        test_obj = SceneObject("test_object", SceneObjectType.ENTITY)
        mesh_c = ModelComponent(test_obj)
        mesh_c.set_mesh_tree(test_obj_mesh)
        mesh_c.lit = True

        trans_c = TransformComponent(test_obj)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        trans_c.transform.orientation = glm.vec3(0, 0, -math.pi / 2)

        cam_c = (CameraComponent(test_obj)
                 .set_distance(0)
                 .set_projection_perspective(config.FOV, config.ASPECT_RATIO, config.VIEW_NEAR, config.VIEW_FAR))

        test_obj.add_component(mesh_c).add_component(trans_c).add_component(cam_c)

        # set up point light 1

        test_light_loader: GltfLoader = GltfLoader("assets/models/light_bulb/bulb.glb")
        test_light_mesh: NodeGraph[MeshNode] = test_light_loader.load()

        light_obj = SceneObject("test_light_1", SceneObjectType.LIGHT)
        light_c = LightComponent(light_obj)
        light_c.set_color(glm.vec3(1, 1, 1)).set_intensity(400).set_attenuation(3).set_type(LightType.point)

        light_trans_c = TransformComponent(light_obj)
        light_trans_c.transform.position = glm.vec3(0, 10, -10)
        light_trans_c.transform.scale = glm.vec3(10, 10, 10)

        light_mesh_c = ModelComponent(light_obj)
        light_mesh_c.set_mesh_tree(test_light_mesh)
        light_mesh_c.lit = False

        light_obj.add_component(light_c).add_component(light_trans_c).add_component(light_mesh_c)

        engine.scene.graph.root.add_child(test_obj).add_child(light_obj)

    def tick(self: Self, delta: int) -> None:
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == ForwardShadedPipeline.Stage.RENDER.value:
            engine.scene.draw_pass(pass_index)
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        gui.scene_graph(engine.scene.graph)
        gui.object_properties()
        return super().draw_gui()

    def event(self: Self, event: pygame.Event) -> None:
        return super().event(event)
