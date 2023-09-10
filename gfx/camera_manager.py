from component.camera_component import CameraComponent
from typing import Self

import core.engine as engine


class CameraManager:
    def __init__(self: Self) -> None:
        self.__camera_cache = list[CameraComponent]()

    def cache_cameras(self: Self) -> None:
        self.__camera_cache = engine.scene.get_from_component_type(CameraComponent)

    def apply_cameras(self: Self) -> None:
        for camera in self.__camera_cache:
            if camera.enabled:
                engine.gfx.push_mat_view(camera.view_matrix)
                engine.gfx.push_mat_proj(camera.proj_matrix)

    def end_cameras(self: Self) -> None:
        for camera in self.__camera_cache:
            if camera.enabled:
                engine.gfx.pop_mat_view()
                engine.gfx.pop_mat_proj()
