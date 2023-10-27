
from component.camera_component import CameraComponent
from component.transform_component import TransformComponent
from typing import Self
from core.app_state import AppState
from core.asset.asset_shader import AssetShader
from scene.scene_object import SceneObject, SceneObjectType
from tests.games.pong.objects.ball import Ball
from tests.games.pong.objects.paddle import Paddle
from tests.games.pong.objects.wall import Wall
from tests.games.pong.pipelines.pong_pipeline import PongPipeline

import glm
import pygame
import gui.gui as gui
import core.engine as engine
import config
import core.asset.asset_manager as asset_manager


class Pong(AppState):
    def init(self: Self) -> None:

        asset_manager.add_asset(AssetShader("pong_post", "assets/shader/pong_post.shader").load())

        engine.gfx.set_pipeline(PongPipeline())

        paddle_1 = Paddle("paddle_1")
        paddle_2 = Paddle("paddle_2")

        wall_left = Wall("wall_left", glm.vec3(-30, 0, 0))
        wall_right = Wall("wall_right", glm.vec3(30, 0, 0))

        ball = Ball("ball")

        camera_obj = SceneObject("camera", SceneObjectType.ENTITY)
        cam_c = (CameraComponent(camera_obj)
                 .set_offset(glm.vec3(0, 8, 14))
                 .set_projection_perspective(config.FOV, config.ASPECT_RATIO, config.VIEW_NEAR, config.VIEW_FAR)
                 .look_at(glm.vec3(0, 0, 0)))
        camera_obj.add_component(cam_c)

        ball.get_component(TransformComponent).set_position(glm.vec3(0, 0, 0))
        paddle_1.get_component(TransformComponent).set_position(glm.vec3(0, 0, -10))
        paddle_2.get_component(TransformComponent).set_position(glm.vec3(0, 0, 10))

        (engine.scene.graph.root
         .add_child(paddle_1)
         .add_child(paddle_2)
         .add_child(wall_left)
         .add_child(wall_right)
         .add_child(ball)
         .add_child(camera_obj))

    def tick(self: Self, delta: int) -> None:
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == PongPipeline.Stage.RENDER.value:
            engine.scene.draw_pass(pass_index)
        if pass_index == PongPipeline.Stage.POST.value:
            pipeline = engine.gfx.get_active_pipeline()
            prev_stage = pipeline.get_last_stage()
            curr_stage = pipeline.get_active_stage()
            curr_stage.render(prev_stage)
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        gui.scene_graph(engine.scene.graph)
        gui.object_properties()
        return super().draw_gui()

    def event(self: Self, event: pygame.Event) -> None:
        return super().event(event)
