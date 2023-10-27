
from typing import Self

import glm
from component.hull_component import HullComponent
from component.rigid_body_component import RigidBodyComponent
from physics.collision_tests import CollisionResult, CollisionTests
from physics.solvers.solver import Solver

from scene.scene_object import SceneObject


class PhysicsWorld:
    def __init__(self: Self) -> None:
        self.objects: list[SceneObject] = []
        self.solvers: list[Solver] = []
        pass

    def physics_tick(self: Self, delta: float) -> None:
        self.solve(delta)
        collisions = self.detect_collisions()
        self.resolve_collisions(collisions)

    def solve(self: Self, delta: float) -> None:
        for solver in self.solvers:
            for obj in self.objects:
                solver.solve(obj, delta)

    def detect_collisions(self: Self) -> list[CollisionResult]:
        result: list[CollisionResult] = []
        tested_pairs: dict[SceneObject, list[SceneObject]] = {}

        # for each obj in the world...
        for obj_a in self.objects:
            if obj_a not in tested_pairs:
                tested_pairs[obj_a] = []
            # test against every other object in the world...
            for obj_b in self.objects:
                if obj_b not in tested_pairs:
                    tested_pairs[obj_b] = []
                if obj_a == obj_b: continue  # don't check collision if objects are same
                if obj_b in tested_pairs[obj_a]: continue
                tested_pairs[obj_a].append(obj_b)
                tested_pairs[obj_b].append(obj_a)
                collision = CollisionTests.test_collision(obj_a, obj_b)
                if collision.is_hit:
                    result.append(collision)

        return result

    def resolve_collisions(self: Self, collisions: list[CollisionResult]) -> None:
        for collision in collisions:
            rb_a = collision.obj_a.get_component(RigidBodyComponent)
            rb_a.acceleration -= collision.hit_normal * glm.length(rb_a.velocity) * 0.9
            pass
        pass

    def add_solver(self: Self, solver: Solver) -> None:
        self.solvers.append(solver)

    def register_object(self: Self, object: SceneObject) -> None:
        self.objects.append(object)
