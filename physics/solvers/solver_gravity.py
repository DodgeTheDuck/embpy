
from typing import Self
from component.rigid_body_component import RigidBodyComponent

from physics.solvers.solver import Solver
from scene.scene_object import SceneObject


class GravitySolver(Solver):
    def __init__(self: Self, force: float) -> None:
        self.force = force
        super().__init__()

    def solve(self: Self, obj: SceneObject, delta: float) -> None:
        rb = obj.get_component(RigidBodyComponent)
        if rb is not None:
            if rb.mass > 0:
                rb.acceleration.y -= self.force
