import random
import glm
import pygame
from component.camera_component import CameraComponent
from component.rigid_body_component import RigidBodyComponent
from component.transform_component import TransformComponent
import gui.gui as gui
import core.engine as engine

from typing import Self
from gfx.pipeline.forward_shaded_pipeline import ForwardShadedPipeline
from core.app_state import AppState
from physics.solvers.solver_gravity import GravitySolver
from tests.physics.collision.objects.ball import Ball
from tests.physics.collision.objects.camera import Camera
from tests.physics.collision.objects.floor import Floor
from tests.physics.collision.objects.light import Light


class CollisionTest(AppState):
    def init(self: Self) -> None:

        engine.gfx.set_pipeline(ForwardShadedPipeline())

        engine.world.add_solver(GravitySolver(9.8))

        # ball_1 = Ball("ball_1").set_color(glm.vec3(1, 0, 0)).set_radius(0.5)
        # ball_1.get_component(TransformComponent).set_position(glm.vec3(0.2, 2, 0))
        # ball_1.get_component(RigidBodyComponent).set_mass(64).set_restitution(0.8)
        # engine.scene.graph.root.add_child(ball_1)
        # engine.world.register_object(ball_1)

        # ball_2 = Ball("ball_2").set_color(glm.vec3(0, 0, 1)).set_radius(0.5)
        # ball_2.get_component(TransformComponent).set_position(glm.vec3(0, 0.6, 0))
        # ball_2.get_component(RigidBodyComponent).set_mass(64).set_restitution(0.8)
        # engine.scene.graph.root.add_child(ball_2)
        # engine.world.register_object(ball_2)

        # ball_2 = Ball(f"ball_1").set_color(glm.vec3(1, 0, 0)).set_radius(0.5)

        for i in range(0, 10):
            r = random.random()
            g = random.random()
            b = random.random()

            x = 8 * random.random() - 4
            y = 4 + 3 * random.random()
            z = 8 * random.random() - 4

            ball = Ball(f"ball_{i}").set_color(glm.vec3(r, g, b)).set_radius(0.5)
            ball.get_component(TransformComponent).set_position(glm.vec3(x, y, z))
            ball.get_component(RigidBodyComponent).set_mass(800).set_restitution(0.8)
            engine.scene.graph.root.add_child(ball)
            engine.world.register_object(ball)

        floor_object = Floor("floor")
        floor_object.get_component(RigidBodyComponent).set_mass(0)

        light_object = Light("light")
        light_object.get_component(TransformComponent).set_position(glm.vec3(0, 30, -10))

        camera_object = Camera("camera")
        camera_object.get_component(CameraComponent).set_position(glm.vec3(0, 1, -5))

        engine.world.register_object(floor_object)

        (engine.scene.graph.root
         .add_child(floor_object)
         .add_child(light_object)
         .add_child(camera_object))

    def tick(self: Self, delta: float) -> None:
        return super().tick(delta)

    def physics_tick(self: Self, delta: float) -> None:
        return super().physics_tick(delta)

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
