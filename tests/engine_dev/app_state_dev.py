

import glm

from typing import Self

import pygame
import gui

from app_state import AppState
from camera import Camera
from component.model_component import ModelComponent
from component.transform_component import TransformComponent
from loaders.gltf_loader import GltfLoader
from mesh import Mesh
from node_graph import NodeGraph
from scene.scene import Scene
from scene.scene_object import SceneObject
import pg

# TODO:
# - move most of the stuff here in to the main engine


class AppStateDev(AppState):
    def init(self: Self) -> None:

        # pygame.mouse.set_visible(False)

        loader: GltfLoader = GltfLoader("models/gltf/barrel/scene.gltf")
        meshes_1: NodeGraph[list[Mesh]] = loader.load()
        # meshes_1: list[Mesh] = loader.load_model("models/gltf/triangle/triangle.gltf")

        self.scene = Scene()

        # lake obj

        test_object = SceneObject("lake scenery")
        mesh_c = ModelComponent(test_object)
        mesh_c.set_mesh_tree(meshes_1)

        trans_c = TransformComponent(test_object)
        trans_c.transform.position = glm.vec3(0, 0, 0)
        #trans_c.transform.scale = glm.vec3(0.2, 0.2, 0.2)

        test_object.add_component(mesh_c)
        test_object.add_component(trans_c)

        self.scene.graph.root.add_child(test_object)

        # setup shader

        # self.prog_scene = pg.gl().add_shader("scene",
        #                                      "scene.frag",
        #                                      "scene.vert")

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
