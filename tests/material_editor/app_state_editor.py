
from typing import Self

import pygame
from gfx.pipeline.basic_shading_pipeline import BasicShadingPipeline
from core.app_state import AppState
from core.camera import Camera
import core.engine as engine


class AppStateMaterialEditor(AppState):
    def init(self: Self) -> None:
        self.camera: Camera = Camera()

    def tick(self: Self, delta: int) -> None:
        self.camera.tick(delta)
        engine.scene.tick(delta)
        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        if pass_index == BasicShadingPipeline.Stage.render:
            engine.scene.draw_geometry()
            pass
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        return super().draw_gui()

    def event(self: Self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                self.camera.mouse_look()
                pass
        return super().event(event)
