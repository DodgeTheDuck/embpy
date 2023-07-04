

import glm

from typing import Self

import pygame

from app_state import AppState
from camera import Camera
from component.mesh import MeshComponent
from component.transform import TransformComponent
from loaders.obj_loader import load_obj
from mesh import Mesh
from scene.scene import Scene
from scene.scene_object import SceneObject
import config
import pg


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # pygame.mouse.set_visible(False)

        monkey: Mesh = load_obj("models/skull.obj")

        self.scene = Scene()

        test_object = SceneObject()
        mesh_c = MeshComponent(test_object)
        mesh_c.set_mesh(monkey)

        trans_c = TransformComponent(test_object)
        trans_c.position = glm.vec3(0, 0, 0)

        test_object.add_component(mesh_c)
        test_object.add_component(trans_c)

        self.scene.graph.root.add_child(test_object)

        # for i in range(-1, 1):
        #     for j in range(-1, 1):
        #         test_object = SceneObject()
        #         mesh_c = MeshComponent(test_object)
        #         mesh_c.set_mesh(monkey)

        #         trans_c = TransformComponent(test_object)
        #         trans_c.position = glm.vec3(i*2, 0, j*2)

        #         test_object.add_component(mesh_c)
        #         test_object.add_component(trans_c)

        #         self.scene.graph.root.add_child(test_object)

        self.prog_scene = pg.gl().add_shader("scene",
                                             "scene.frag",
                                             "scene.vert")

        pg.gl().use_program(self.prog_scene)

        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        self.scene.tick(delta)
        pygame.mouse.set_pos(config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2)
        return super().tick(delta)

    def draw(self: Self, delta: int) -> None:
        pg.gl().push_mat_view(self.camera.transform)
        pg.gl().push_mat_proj(self.camera.projection)
        self.scene.draw(delta)
        pg.gl().pop_mat_proj()
        pg.gl().pop_mat_view()
        return super().draw(delta)

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                self.camera.mouse_look()
                pass
        return super().event(event)
