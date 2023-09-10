import math
from typing import Self

import glm
import pygame
from component.component import Component
from scene.scene_object import SceneObject


class CameraComponent(Component):
    def __init__(self: Self, owner: SceneObject) -> None:
        self.offset = glm.vec3(0, 0, 0)
        self.yaw = 0
        self.pitch = 0
        self.view_matrix = glm.mat4()
        self.proj_matrix = glm.mat4()
        self.enabled = True
        self.position = glm.vec3(0, 0, 0)

        self.is_free = False
        self.free_move_speed = 30

        super().__init__(owner, "Camera")

    def set_projection_perspective(self: Self, fov: float, aspect_ratio: float, near: float, far: float) -> Self:
        self.proj_matrix = glm.perspective(fov, aspect_ratio, near, far)
        return self

    def set_offset(self: Self, offset: glm.vec3) -> Self:
        self.offset = offset
        return self

    def look_at(self: Self, location: glm.vec3) -> Self:
        self.view_matrix = glm.lookAt(self.offset,
                                      location,
                                      glm.vec3(0, 1, 0))
        return self

    def tick(self: Self, delta: float) -> None:

        if self.is_free:
            keys: list[int] = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.yaw += 90 * delta
            if keys[pygame.K_RIGHT]:
                self.yaw -= 90 * delta
            if keys[pygame.K_UP]:
                self.pitch += 90 * delta
            if keys[pygame.K_DOWN]:
                self.pitch -= 90 * delta

            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

            yaw_rads = glm.radians(self.yaw)
            pitch_rads = glm.radians(self.pitch)

            front = glm.vec3()
            front.x = glm.cos(pitch_rads) * glm.sin(yaw_rads)
            front.y = glm.sin(pitch_rads)
            front.z = glm.cos(pitch_rads) * glm.cos(yaw_rads)

            right = glm.vec3()
            right.x = glm.sin(yaw_rads - math.pi / 2)
            right.y = 0
            right.z = glm.cos(yaw_rads - math.pi / 2)

            up = glm.cross(right, front)

            if keys[pygame.K_w]:
                self.position += front * self.free_move_speed * delta
            if keys[pygame.K_s]:
                self.position -= front * self.free_move_speed * delta
            if keys[pygame.K_a]:
                self.position -= right * self.free_move_speed * delta
            if keys[pygame.K_d]:
                self.position += right * self.free_move_speed * delta
            if keys[pygame.K_q]:
                self.position.y += self.free_move_speed * delta
            if keys[pygame.K_e]:
                self.position.y -= self.free_move_speed * delta

            self.view_matrix = glm.lookAt(self.position,
                                          self.position + front,
                                          up)

        return super().tick(delta)

    def draw_pass(self: Self, pass_index: int) -> None:
        return super().draw_pass(pass_index)

    def draw_gui(self: Self) -> None:
        return super().draw_gui()
