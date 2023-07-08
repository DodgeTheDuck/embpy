import math
from typing import Self
import glm
import OpenGL.GL as gl
import pygame
import input
import config
import pg


class Camera:
    def __init__(self: Self) -> None:
        self.transform: glm.mat4 = glm.lookAt(glm.vec3(5, 5, 5),
                                              glm.vec3(0, 0, 0),
                                              glm.vec3(0, 1, 0))
        self.projection: glm.mat4 = glm.perspective(glm.radians(config.FOV),
                                                    config.ASPECT_RATIO,
                                                    config.VIEW_NEAR,
                                                    config.VIEW_FAR)
        self.position = glm.vec3(0, 5, 0)
        self.move_speed = 1
        self.sensitivity = 0.5
        self.yaw = 0
        self.pitch = 0

    def mouse_look(self: Self) -> None:
        x_offset = self.sensitivity * input.mouse().delta_x
        y_offset = self.sensitivity * input.mouse().delta_y
        self.yaw -= x_offset
        self.pitch -= y_offset

    def tick(self: Self, delta: float) -> None:
        keys: list[int] = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.z += self.move_speed * delta
        if keys[pygame.K_s]:
            self.position.z -= self.move_speed * delta
        if keys[pygame.K_a]:
            self.position.x += self.move_speed * delta
        if keys[pygame.K_d]:
            self.position.x -= self.move_speed * delta
        if keys[pygame.K_q]:
            self.position.y += self.move_speed * delta
        if keys[pygame.K_e]:
            self.position.y -= self.move_speed * delta

        if keys[pygame.K_LEFT]:
            self.yaw -= 90 * delta
        if keys[pygame.K_RIGHT]:
            self.yaw += 90 * delta
        if keys[pygame.K_UP]:
            self.pitch -= 90 * delta
        if keys[pygame.K_DOWN]:
            self.pitch += 90 * delta

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

        self.transform = glm.lookAt(self.position,
                                    self.position + front,
                                    up)

        # TODO: not have this part here
        gl.glUniform3f(gl.glGetUniformLocation(pg.gl().get_program("scene"),
                                               "viewPos"),
                       self.position.x,
                       self.position.y,
                       self.position.z)
