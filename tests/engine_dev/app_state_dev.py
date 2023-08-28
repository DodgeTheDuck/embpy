import glm
import pygame
import gui.gui as gui
import core.engine as engine

from typing import Self
from component.light_component import LightComponent, LightType
from gfx.pipeline.forward_shaded_pipeline import ForwardShadedPipeline
from gfx.mesh_node import MeshNode
from core.app_state import AppState
from core.camera import Camera
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from loaders.gltf_loader import GltfLoader
from core.node_graph import NodeGraph
from scene.obj_sky_box import ObjSkyBox
from scene.scene_object import SceneObject, SceneObjectType


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # set up test model

        engine.gfx.set_pipeline(ForwardShadedPipeline())

        test_obj_loader: GltfLoader = GltfLoader("assets/models/house/house.glb")
        test_obj_mesh: NodeGraph[MeshNode] = test_obj_loader.load()

        test_obj = SceneObject("test_object", SceneObjectType.ENTITY)
        mesh_c = ModelComponent(test_obj)
        mesh_c.set_mesh_tree(test_obj_mesh)
        mesh_c.shaded = True

        trans_c = TransformComponent(test_obj)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        trans_c.transform.scale = glm.vec3(10, 10, 10)
        trans_c.transform.orientation = glm.vec3(0, 0, 0)

        test_obj.add_component(mesh_c).add_component(trans_c)

        # set up point light 1

        test_light_loader: GltfLoader = GltfLoader("assets/models/light_bulb/bulb.glb")
        test_light_mesh: NodeGraph[MeshNode] = test_light_loader.load()

        light_obj = SceneObject("test_light_1", SceneObjectType.LIGHT)
        light_c = LightComponent(light_obj)
        light_c.set_color(glm.vec3(1, 1, 1)).set_intensity(400).set_attenuation(0.01).set_type(LightType.point)

        light_trans_c = TransformComponent(light_obj)
        light_trans_c.transform.position = glm.vec3(80, 80, 80)
        light_trans_c.transform.scale = glm.vec3(10, 10, 10)

        light_mesh_c = ModelComponent(light_obj)
        light_mesh_c.set_mesh_tree(test_light_mesh)
        light_mesh_c.shaded = False

        light_obj.add_component(light_c).add_component(light_trans_c).add_component(light_mesh_c)

        # set up skybox

        sky_box_obj = ObjSkyBox("sky_box")

        engine.scene.graph.root.add_child(test_obj).add_child(light_obj).add_child(sky_box_obj)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == ForwardShadedPipeline.Stage.RENDER.value:
            engine.gfx.push_mat_view(self.camera.transform)
            engine.gfx.push_mat_proj(self.camera.projection)
            engine.scene.draw_pass(pass_index)
            engine.gfx.pop_mat_proj
            engine.gfx.pop_mat_view()
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        gui.scene_graph(engine.scene.graph)
        gui.object_properties()
        self.camera.draw_gui()
        return super().draw_gui()

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                self.camera.mouse_look()
                pass
        return super().event(event)
