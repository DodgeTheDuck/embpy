

import math
import glm

from typing import Self

import pygame
from component.light_component import LightComponent
from gfx.mesh_node import MeshNode
import gui.gui as gui

from core.app_state import AppState
from core.camera import Camera
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from loaders.gltf_loader import GltfLoader
from gfx.mesh import Mesh
from core.node_graph import NodeGraph
from scene.scene_object import SceneObject, SceneObjectType
import OpenGL.GL as gl
import core.pg as pg
import core.engine as engine

# TODO:
# - move most of the stuff here in to the main engine


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # set up test model

        loader: GltfLoader = GltfLoader("models/gltf/roman_armour/armour.glb")
        armour_mesh: NodeGraph[MeshNode] = loader.load()

        armour_obj = SceneObject("test object", SceneObjectType.entity)
        mesh_c = ModelComponent(armour_obj)
        mesh_c.set_mesh_tree(armour_mesh)

        trans_c = TransformComponent(armour_obj)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        trans_c.transform.orientation = glm.vec3(0, math.pi, 0)

        armour_obj.add_component(mesh_c).add_component(trans_c)

        # set up light

        loader: GltfLoader = GltfLoader("models/gltf/light_volumes/point_light.glb")
        light_volume: NodeGraph[MeshNode] = loader.load()

        light_obj = SceneObject("test light", SceneObjectType.light)
        light_c = LightComponent(light_obj)
        light_c.set_volume_mesh(light_volume)

        light_trans_c = TransformComponent(light_obj)
        light_trans_c.transform.scale = glm.vec3(100, 100, 100)

        light_obj.add_component(light_c).add_component(light_trans_c)

        engine.scene.graph.root.add_child(armour_obj).add_child(light_obj)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_geometry(self: Self) -> None:


        pg.gl().push_mat_view(self.camera.transform)
        pg.gl().push_mat_proj(self.camera.projection)
        engine.scene.draw_geometry()
        pg.gl().pop_mat_proj()
        pg.gl().pop_mat_view()
        return super().draw_geometry()

    def draw_lighting(self: Self) -> None:
        pg.gl().push_mat_view(self.camera.transform)
        pg.gl().push_mat_proj(self.camera.projection)
        engine.scene.draw_lighting()
        pg.gl().pop_mat_proj()
        pg.gl().pop_mat_view()
        return super().draw_lighting()

    def draw_camera(self: Self) -> None:

        gl.glUniform3f(pg.gl().top_pipeline_stage().draw_shader.get_uniform_loc("viewPos"),
                       self.camera.position.x,
                       self.camera.position.y,
                       self.camera.position.z)

        return super().draw_lighting()

    def gui(self: Self) -> None:
        gui.scene_graph(engine.scene.graph)
        gui.object_properties()
        return super().gui()

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                self.camera.mouse_look()
                pass
        return super().event(event)
