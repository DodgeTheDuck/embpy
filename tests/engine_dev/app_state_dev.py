

import glm

from typing import Self

import pygame
import gui

from app_state import AppState
from camera import Camera
from component.model import ModelComponent
from component.transform import TransformComponent
from loaders.obj_loader import load_obj
from mesh import Mesh
from scene.scene import Scene
from scene.scene_object import SceneObject
import pg

# TODO:
# - move most of the stuff here in to the main engine


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # pygame.mouse.set_visible(False)

        meshes_1: list[Mesh] = load_obj("models/lake scenery.obj")
        meshes_2: list[Mesh] = load_obj("models/rubberduck.obj")

        self.scene = Scene()

        # lake obj

        test_object = SceneObject("lake scene")
        mesh_c = ModelComponent(test_object)
        mesh_c.set_meshes(meshes_1)

        trans_c = TransformComponent(test_object)
        trans_c.position = glm.vec3(0, 0, 0)

        test_object.add_component(mesh_c)
        test_object.add_component(trans_c)

        self.scene.graph.root.add_child(test_object)

        # duck obj

        test_object_2 = SceneObject("duck")
        mesh_c_2 = ModelComponent(test_object_2)
        mesh_c_2.set_meshes(meshes_2)

        trans_c_2 = TransformComponent(test_object_2)
        trans_c_2.position = glm.vec3(0, 1, 0)
        trans_c_2.scale = glm.vec3(0.05, 0.05, 0.05)

        test_object_2.add_component(mesh_c_2)
        test_object_2.add_component(trans_c_2)

        self.scene.graph.root.add_child(test_object_2)

        # duck obj 2

        test_object_3 = SceneObject("duck_2")
        mesh_c_3 = ModelComponent(test_object_3)
        mesh_c_3.set_meshes(meshes_2)

        trans_c_3 = TransformComponent(test_object_3)
        trans_c_3.position = glm.vec3(0, 1, 0)
        trans_c_3.scale = glm.vec3(0.05, 0.05, 0.05)

        test_object_3.add_component(mesh_c_3)
        test_object_3.add_component(trans_c_3)

        test_object_2.add_child(test_object_3)

        # setup shader

        self.prog_scene = pg.gl().add_shader("scene",
                                             "scene.frag",
                                             "scene.vert")

        pg.gl().use_program(self.prog_scene)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        self.scene.tick(delta)
        # pygame.mouse.set_pos(config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2)
        return super().tick(delta)

    def draw(self: Self, delta: int) -> None:
        pg.gl().push_mat_view(self.camera.transform)
        pg.gl().push_mat_proj(self.camera.projection)
        self.scene.draw(delta)
        pg.gl().pop_mat_proj()
        pg.gl().pop_mat_view()
        return super().draw(delta)

    def gui(self: Self) -> None:
        gui.scene_graph(self.scene.graph)
        gui.object_properties()
        return super().gui()

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                # self.camera.mouse_look()
                pass
        return super().event(event)
